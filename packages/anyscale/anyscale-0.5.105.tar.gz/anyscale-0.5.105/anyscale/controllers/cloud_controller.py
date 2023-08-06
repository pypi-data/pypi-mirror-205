"""
Fetches data required and formats output for `anyscale cloud` commands.
"""

from datetime import timedelta
import ipaddress
import json
from os import getenv
import re
import secrets
import time
from typing import Any, Dict, List, Optional, Tuple

import boto3
from botocore.exceptions import ClientError
import click
from click import ClickException, INT, prompt

from anyscale.aws_iam_policies import (
    ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN,
    ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE,
    ANYSCALE_IAM_PERMISSIONS_SERVICE_STEADY_STATE,
    ANYSCALE_SSM_READ_WRITE_ACCESS_POLICY_DOCUMENT,
    ANYSCALE_SSM_READONLY_ACCESS_POLICY_DOCUMENT,
)
from anyscale.cli_logger import BlockLogger, LogsLogger
from anyscale.client.openapi_client.models import (
    CloudConfig,
    CloudWithCloudResource,
    ClusterManagementStackVersions,
    CreateCloudResource,
    CreateCloudResourceGCP,
    UpdateCloudWithCloudResource,
    UpdateCloudWithCloudResourceGCP,
    WriteCloud,
)
from anyscale.client.openapi_client.models.cloud_state import CloudState
from anyscale.client.openapi_client.models.subnet_id_with_availability_zone_aws import (
    SubnetIdWithAvailabilityZoneAWS,
)
from anyscale.cloud import (
    get_cloud_id_and_name,
    get_cloud_json_from_id,
    get_cloud_resource_by_cloud_id,
    get_organization_id,
)
from anyscale.cloud_resource import (
    associate_aws_subnets_with_azs,
    verify_aws_cloudformation_stack,
    verify_aws_efs,
    verify_aws_iam_roles,
    verify_aws_s3,
    verify_aws_security_groups,
    verify_aws_subnets,
    verify_aws_vpc,
)
from anyscale.conf import ANYSCALE_IAM_ROLE_NAME
from anyscale.controllers.base_controller import BaseController
from anyscale.formatters import clouds_formatter
from anyscale.shared_anyscale_utils.aws import AwsRoleArn, get_dataplane_role_arn
from anyscale.shared_anyscale_utils.conf import ANYSCALE_ENV
from anyscale.util import (  # pylint:disable=private-import
    _client,
    _get_aws_efs_mount_target_ip,
    _get_role,
    _update_external_ids_for_policy,
    confirm,
    get_available_regions,
    get_user_env_aws_account,
    launch_gcp_cloud_setup,
    prepare_cloudformation_template,
)
from anyscale.utils.cloud_utils import verify_anyscale_access
from anyscale.utils.imports.gcp import (
    try_import_gcp_discovery,
    try_import_gcp_managed_setup_utils,
    try_import_gcp_utils,
    try_import_gcp_verify_lib,
)


WAIT_FOR_ACTIVE_CLOUD_RETRIES = 120
ROLE_CREATION_RETRIES = 30
ROLE_CREATION_INTERVAL_SECONDS = 1
try:
    CLOUDFORMATION_TIMEOUT_SECONDS = int(getenv("CLOUDFORMATION_TIMEOUT_SECONDS", 300))
except ValueError:
    raise Exception(
        f"CLOUDFORMATION_TIMEOUT_SECONDS is set to {getenv('CLOUDFORMATION_TIMEOUT_SECONDS')}, which is not a valid integer."
    )

IGNORE_CAPACITY_ERRORS = getenv("IGNORE_CAPACITY_ERRORS") is not None

# Constants forked from ray.autoscaler._private.aws.config
RAY = "ray-autoscaler"
DEFAULT_RAY_IAM_ROLE = RAY + "-v1"


class CloudController(BaseController):
    def __init__(
        self, log: Optional[LogsLogger] = None, initialize_auth_api_client: bool = True
    ):
        if log is None:
            log = LogsLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log
        self.log.open_block("Output")

    def list_clouds(self, cloud_name: Optional[str], cloud_id: Optional[str]) -> str:
        if cloud_id is not None:
            clouds = [
                self.api_client.get_cloud_api_v2_clouds_cloud_id_get(cloud_id).result
            ]
        elif cloud_name is not None:
            clouds = [
                self.api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post(
                    {"name": cloud_name}
                ).result
            ]
        else:
            clouds = self.api_client.list_clouds_api_v2_clouds_get().results
        output = clouds_formatter.format_clouds_output(clouds=clouds, json_format=False)

        return str(output)

    def verify_vpc_peering(
        self,
        yes: bool,
        vpc_peering_ip_range: Optional[str],
        vpc_peering_target_project_id: Optional[str],
        vpc_peering_target_vpc_id: Optional[str],
    ) -> None:
        if (
            vpc_peering_ip_range
            or vpc_peering_target_project_id
            or vpc_peering_target_vpc_id
        ):
            if not vpc_peering_ip_range:
                raise ClickException("Please specify a VPC peering IP range.")
            if not vpc_peering_target_project_id:
                raise ClickException("Please specify a VPC peering target project ID.")
            if not vpc_peering_target_vpc_id:
                raise ClickException("Please specify a VPC peering target VPC ID.")
        else:
            return

        try:
            valid_ip_network = ipaddress.IPv4Network(vpc_peering_ip_range)
        except ValueError:
            raise ClickException(f"{vpc_peering_ip_range} is not a valid IP address.")
        # https://cloud.google.com/vpc/docs/vpc#valid-ranges
        allowed_ip_ranges = [
            ipaddress.IPv4Network("10.0.0.0/8"),
            ipaddress.IPv4Network("172.16.0.0/12"),
            ipaddress.IPv4Network("192.168.0.0/16"),
        ]

        for allowed_ip_range in allowed_ip_ranges:
            if valid_ip_network.subnet_of(allowed_ip_range):
                break
        else:
            raise ClickException(
                f"{vpc_peering_ip_range} is not a allowed private IP address range for GCP. The allowed IP ranges are 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16. For more info, see https://cloud.google.com/vpc/docs/vpc#valid-ranges"
            )

        if (
            valid_ip_network.num_addresses
            < ipaddress.IPv4Network("192.168.0.0/16").num_addresses
        ):
            raise ClickException(
                f"{vpc_peering_ip_range} is not a valid IP range. The minimum size is /16"
            )

        if not yes:
            confirm(
                f"\nYou selected to create a VPC peering connection to VPC {vpc_peering_target_vpc_id} in GCP project {vpc_peering_target_project_id}."
                f"This will create a VPC peering connection from your Anyscale GCP project to the target project ({vpc_peering_target_project_id})."
                "You will need to manually create the peering connection from the target project to your Anyscale GCP project after the anyscale cloud is created.\n"
                "Continue cloud setup?",
                False,
            )

    def setup_cloud(  # noqa: PLR0913
        self,
        provider: str,
        region: Optional[str],
        name: str,
        yes: bool = False,
        gce: bool = False,
        folder_id: Optional[int] = None,
        vpc_peering_ip_range: Optional[str] = None,
        vpc_peering_target_project_id: Optional[str] = None,
        vpc_peering_target_vpc_id: Optional[str] = None,
    ) -> None:
        """
        Sets up a cloud provider
        """
        if provider == "gcp":
            # If the region is blank, change it to the default for GCP.
            if region is None:
                region = "us-west1"
            # Warn the user about a bad region before the cloud configuration begins.
            # GCP's `list regions` API requires a project, meaning true verification
            # happens in the middle of the flow.
            gcp_regions = (
                self.api_client.get_regions_and_zones_api_v2_clouds_gcp_regions_and_zones_get().result.regions.keys()
            )
            if region not in gcp_regions and not yes:
                confirm(
                    f"You selected the region: {region}, but it is not in"
                    f"the cached list of GCP regions:\n\n{sorted(gcp_regions)}.\n"
                    "Continue cloud setup with this region?",
                    False,
                )
            if not yes and not folder_id:
                folder_id = prompt(
                    "Please select the GCP Folder ID where the 'Anyscale' folder will be created.\n"
                    "\tYour GCP account must have permissions to create sub-folders in the specified folder.\n"
                    "\tView your organization's folder layout here: https://console.cloud.google.com/cloud-resource-manager\n"
                    "\tIf not specified, the 'Anyscale' folder will be created directly under the organization.\n"
                    "Folder ID (numerals only)",
                    default="",
                    type=INT,
                    show_default=False,
                )

            self.verify_vpc_peering(
                yes,
                vpc_peering_ip_range,
                vpc_peering_target_project_id,
                vpc_peering_target_vpc_id,
            )
            # TODO: interactive setup process through the CLI?
            launch_gcp_cloud_setup(
                name=name,
                region=region,
                is_k8s=not gce,
                folder_id=folder_id,
                vpc_peering_ip_range=vpc_peering_ip_range,
                vpc_peering_target_project_id=vpc_peering_target_project_id,
                vpc_peering_target_vpc_id=vpc_peering_target_vpc_id,
            )
        else:
            raise ClickException(
                f'Invalid Cloud provider: {provider}; only "gcp" is supported.'
            )

    def run_cloudformation(
        self,
        region: str,
        cloud_id: str,
        anyscale_iam_role_name: str,
        cluster_node_iam_role_name: str,
    ) -> Dict[str, Any]:
        response = (
            self.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get()
        )

        anyscale_aws_account = response.result.anyscale_aws_account
        cfn_client = _client("cloudformation", region)
        cfn_stack_name = cloud_id.replace("_", "-").lower()

        cfn_template_body = prepare_cloudformation_template(
            region, cfn_stack_name, cloud_id
        )

        self.log.debug("cloudformation body:")
        self.log.debug(cfn_template_body)

        cfn_client.create_stack(
            StackName=cfn_stack_name,
            TemplateBody=cfn_template_body,
            Parameters=[
                {"ParameterKey": "EnvironmentName", "ParameterValue": ANYSCALE_ENV},
                {"ParameterKey": "CloudID", "ParameterValue": cloud_id},
                {
                    "ParameterKey": "AnyscaleAWSAccountID",
                    "ParameterValue": anyscale_aws_account,
                },
                {
                    "ParameterKey": "AnyscaleCrossAccountIAMRoleName",
                    "ParameterValue": anyscale_iam_role_name,
                },
                {
                    "ParameterKey": "AnyscaleCrossAccountIAMPolicySteadyState",
                    "ParameterValue": json.dumps(
                        ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE
                    ),
                },
                {
                    "ParameterKey": "AnyscaleCrossAccountIAMPolicyServiceSteadyState",
                    "ParameterValue": json.dumps(
                        ANYSCALE_IAM_PERMISSIONS_SERVICE_STEADY_STATE
                    ),
                },
                {
                    "ParameterKey": "AnyscaleCrossAccountIAMPolicyInitialRun",
                    "ParameterValue": json.dumps(
                        ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN
                    ),
                },
                {
                    "ParameterKey": "ClusterNodeIAMRoleName",
                    "ParameterValue": cluster_node_iam_role_name,
                },
            ],
            Capabilities=["CAPABILITY_NAMED_IAM", "CAPABILITY_AUTO_EXPAND"],
        )

        stacks = cfn_client.describe_stacks(StackName=cfn_stack_name)
        cfn_stack = stacks["Stacks"][0]
        cfn_stack_url = f"https://{region}.console.aws.amazon.com/cloudformation/home?region={region}#/stacks/stackinfo?stackId={cfn_stack['StackId']}"
        self.log.info(f"\nTrack progress of cloudformation at {cfn_stack_url}")
        with self.log.spinner("Creating cloud resources through cloudformation..."):
            start_time = time.time()
            end_time = start_time + CLOUDFORMATION_TIMEOUT_SECONDS
            while time.time() < end_time:
                stacks = cfn_client.describe_stacks(StackName=cfn_stack_name)
                cfn_stack = stacks["Stacks"][0]
                if cfn_stack["StackStatus"] in (
                    "CREATE_FAILED",
                    "ROLLBACK_COMPLETE",
                    "ROLLBACK_IN_PROGRESS",
                ):
                    bucket_name = f"anyscale-{ANYSCALE_ENV}-data-{cfn_stack_name}"
                    try:
                        _client("s3", region).delete_bucket(Bucket=bucket_name)
                        self.log.info(f"Successfully deleted {bucket_name}")
                    except Exception as e:  # noqa: BLE001
                        if not (
                            isinstance(e, ClientError)
                            and e.response["Error"]["Code"] == "NoSuckBucket"
                        ):
                            self.log.error(
                                f"Unable to delete the S3 bucket created by the cloud formation stack, please manually delete {bucket_name}"
                            )

                    # Provide link to cloudformation
                    raise ClickException(
                        f"Failed to set up cloud resources. Please check your cloudformation stack for errors and to ensure that all resources created in this cloudformation stack were deleted: {cfn_stack_url}"
                    )
                if cfn_stack["StackStatus"] == "CREATE_COMPLETE":
                    self.log.info(
                        f"Cloudformation stack {cfn_stack['StackId']} Completed"
                    )
                    break

                time.sleep(1)

            if time.time() > end_time:
                raise ClickException(
                    f"Timed out creating AWS resources. Please check your cloudformation stack for errors. {cfn_stack['StackId']}"
                )
        return cfn_stack

    def update_cloud_with_resources(self, cfn_stack: Dict[str, Any], cloud_id: str):
        if "Outputs" not in cfn_stack:
            raise ClickException(
                f"Timed out setting up cloud resources. Please check your cloudformation stack for errors. {cfn_stack['StackId']}"
            )

        cfn_resources = {}
        for resource in cfn_stack["Outputs"]:
            resource_type = resource["OutputKey"]
            resource_value = resource["OutputValue"]
            assert (
                resource_value is not None
            ), f"{resource_type} is not created properly. Please delete the cloud and try creating agian."
            cfn_resources[resource_type] = resource_value

        aws_subnets_with_availability_zones = json.loads(
            cfn_resources["SubnetsWithAvailabilityZones"]
        )
        aws_vpc_id = cfn_resources["VPC"]
        aws_security_groups = [cfn_resources["AnyscaleSecurityGroup"]]
        aws_s3_id = cfn_resources["S3Bucket"]
        aws_efs_id = cfn_resources["EFS"]
        aws_efs_mount_target_ip = cfn_resources["EFSMountTargetIP"]
        anyscale_iam_role_arn = cfn_resources["AnyscaleIAMRole"]
        cluster_node_iam_role_arn = cfn_resources["NodeIamRole"]

        create_cloud_resource = CreateCloudResource(
            aws_vpc_id=aws_vpc_id,
            aws_subnet_ids_with_availability_zones=[
                SubnetIdWithAvailabilityZoneAWS(
                    subnet_id=subnet_with_az["subnet_id"],
                    availability_zone=subnet_with_az["availability_zone"],
                )
                for subnet_with_az in aws_subnets_with_availability_zones
            ],
            aws_iam_role_arns=[anyscale_iam_role_arn, cluster_node_iam_role_arn],
            aws_security_groups=aws_security_groups,
            aws_s3_id=aws_s3_id,
            aws_efs_id=aws_efs_id,
            aws_efs_mount_target_ip=aws_efs_mount_target_ip,
            aws_cloudformation_stack_id=cfn_stack["StackId"],
        )

        self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put(
            cloud_id=cloud_id,
            update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
                cloud_resource_to_update=create_cloud_resource
            ),
        )

    def prepare_for_managed_cloud_setup(
        self,
        region: str,
        cloud_name: str,
        cluster_management_stack_version: ClusterManagementStackVersions,
    ) -> Tuple[str, str]:
        regions_available = get_available_regions()
        if region not in regions_available:
            raise ClickException(
                f"Region '{region}' is not available. Regions available are: "
                f"{', '.join(map(repr, regions_available))}"
            )

        for _ in range(5):
            anyscale_iam_role_name = "{}-{}".format(
                ANYSCALE_IAM_ROLE_NAME, secrets.token_hex(4)
            )

            role = _get_role(anyscale_iam_role_name, region)
            if role is None:
                break
        else:
            raise RuntimeError(
                "We weren't able to connect your account with the Anyscale because we weren't able to find an available IAM Role name in your account. Please reach out to support or your SA for assistance."
            )

        user_aws_account_id = get_user_env_aws_account(region)
        try:
            created_cloud = self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    provider="AWS",
                    region=region,
                    credentials=AwsRoleArn.from_role_name(
                        user_aws_account_id, anyscale_iam_role_name
                    ).to_string(),
                    name=cloud_name,
                    is_bring_your_own_resource=False,
                    cluster_management_stack_version=cluster_management_stack_version,
                )
            ).result
        except ClickException as e:
            if "409" in e.message:
                raise ClickException(
                    f"Cloud with name {cloud_name} already exists. Please choose a different name."
                )
            raise

        return anyscale_iam_role_name, created_cloud.id

    def prepare_for_managed_cloud_setup_gcp(
        self,
        project_id: str,
        region: str,
        cloud_name: str,
        factory: Any,
        cluster_management_stack_version: ClusterManagementStackVersions,
    ):
        setup_utils = try_import_gcp_managed_setup_utils()

        # choose an service account name and create a provider pool
        for _ in range(5):
            token = secrets.token_hex(4)
            anyscale_access_service_account = (
                f"anyscale-access-{token}@{project_id}.iam.gserviceaccount.com"
            )
            service_account = setup_utils.get_anyscale_gcp_access_service_acount(
                factory, anyscale_access_service_account
            )
            if service_account is not None:
                continue
            pool_id = f"anyscale-provider-pool-{token}"
            wordload_identity_pool = setup_utils.get_workload_identity_pool(
                factory, project_id, pool_id
            )
            if wordload_identity_pool is None:
                break
        else:
            raise ClickException(
                "We weren't able to connect your account with the Anyscale because we weren't able to find an available serivce account name and create a provider pool in your GCP project. Please reach out to support or your SA for assistance."
            )

        # build credentials
        project_number = setup_utils.get_project_number(factory, project_id)
        provider_id = "anyscale-access"
        provider_name = f"{project_number}/locations/global/workloadIdentityPools/{pool_id}/providers/{provider_id}"
        credentials = json.dumps(
            {
                "project_id": project_id,
                "provider_id": provider_name,
                "service_account_email": anyscale_access_service_account,
            }
        )

        # create a cloud
        try:
            created_cloud = self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    provider="GCP",
                    region=region,
                    credentials=credentials,
                    name=cloud_name,
                    is_bring_your_own_resource=False,
                    cluster_management_stack_version=cluster_management_stack_version,
                )
            ).result
        except ClickException as e:
            if "409" in e.message:
                raise ClickException(
                    f"Cloud with name {cloud_name} already exists. Please choose a different name."
                )
            raise
        return anyscale_access_service_account, pool_id, created_cloud.id

    def create_workload_identity_federation_provider(
        self,
        factory: Any,
        project_id: str,
        pool_id: str,
        anyscale_access_service_account: str,
    ):
        setup_utils = try_import_gcp_managed_setup_utils()

        # create provider pool
        pool_display_name = "Anyscale provider pool"
        pool_description = f"Workload Identity Provider Pool for Anyscale access service account {anyscale_access_service_account}"

        wordload_identity_pool = setup_utils.create_workload_identity_pool(
            factory, project_id, pool_id, self.log, pool_display_name, pool_description,
        )

        try:
            # create provider
            provider_display_name = "Anyscale Access"
            provider_id = "anyscale-access"
            anyscale_aws_account = (
                self.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get().result.anyscale_aws_account
            )
            organization_id = get_organization_id(self.api_client)
            setup_utils.create_anyscale_aws_provider(
                factory,
                organization_id,
                wordload_identity_pool,
                provider_id,
                anyscale_aws_account,
                provider_display_name,
                self.log,
            )
        except ClickException as e:
            # delete provider pool if there's an exception
            setup_utils.delete_workload_identity_pool(
                factory, wordload_identity_pool, self.log
            )
            # TODO (congding): delete cloud in `setup_managed_cloud` method
            raise ClickException(
                f"Error occurred when trying to set up workload identity federation: {e}"
            )

    def wait_for_cloud_to_be_active(self, cloud_id: str) -> None:
        """
        Waits for the cloud to be active
        """
        with self.log.spinner("Setting up resources on anyscale for your new cloud..."):
            try:
                # This call will get or create the provider metadata for the cloud.
                # Note that this is a blocking call and can take over 60s to complete. This is because we're currently fetching cloud
                # provider metadata in every region, which isn't necessary for cloud setup.
                # TODO (allen): only fetch the provider metadata for the region that the cloud is in.
                self.api_client.get_provider_metadata_api_v2_clouds_provider_metadata_cloud_id_get(
                    cloud_id, max_staleness=int(timedelta(hours=1).total_seconds()),
                )
            except Exception as e:  # noqa: BLE001
                self.log.error(
                    f"Failed to get cloud provider metadata. Your cloud may not be set up properly. Please reach out to Anyscale support for assistance. Error: {e}"
                )

            for _ in range(WAIT_FOR_ACTIVE_CLOUD_RETRIES):
                cloud = self.api_client.get_cloud_api_v2_clouds_cloud_id_get(cloud_id)
                if cloud.result.state == CloudState.ACTIVE:
                    break
                elif cloud.result.state == CloudState.VERIFICATION_FAILED:
                    self.log.error(
                        "Cloud state is `VERIFICATION_FAILED`. Your cloud may not be set up properly. Please reach out to Anyscale support for assistance."
                    )
                    break
                time.sleep(1)
            else:
                self.log.error(
                    "Timed out waiting for the cloud to become active. Your cloud may not be set up properly. Please reach out to Anyscale support for assistance."
                )

    def setup_managed_cloud(
        self,
        provider: str,
        region: str,
        name: str,
        cluster_management_stack_version: ClusterManagementStackVersions,
    ) -> None:
        """
        Sets up a cloud provider
        """
        if provider == "aws":
            with self.log.spinner("Preparing environment for cloud setup..."):
                (
                    anyscale_iam_role_name,
                    cloud_id,
                ) = self.prepare_for_managed_cloud_setup(
                    region, name, cluster_management_stack_version
                )

            try:
                cfn_stack = self.run_cloudformation(
                    region,
                    cloud_id,
                    anyscale_iam_role_name,
                    f"{cloud_id}-cluster_node_role",
                )
                self.update_cloud_with_resources(cfn_stack, cloud_id)
                self.wait_for_cloud_to_be_active(cloud_id)
            except Exception as e:  # noqa: BLE001
                self.log.error(str(e))
                self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                    cloud_id=cloud_id
                )
                raise ClickException("Cloud setup failed!")

            self.log.info(f"Successfully created cloud {name}, and it's ready to use.")
        elif provider == "gcp":
            # TODO (allenyin): Implement for GCP.
            raise ClickException(
                "Managed cloud creation for GCP is not currently supported."
            )
        else:
            raise ClickException(
                f"Invalid Cloud provider: {provider}. Available providers are [aws, gcp]."
            )

    def update_cloud_config(
        self,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        max_stopped_instances: int,
    ) -> None:
        """Updates a cloud's configuration by name or id.

        Currently the only supported option is "max_stopped_instances."
        """

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        self.api_client.update_cloud_config_api_v2_clouds_cloud_id_config_put(
            cloud_id=cloud_id,
            cloud_config=CloudConfig(max_stopped_instances=max_stopped_instances),
        )

        self.log.info(f"Updated config for cloud '{cloud_name}' to:")
        self.log.info(self.get_cloud_config(cloud_name=None, cloud_id=cloud_id))

    def get_cloud_config(
        self, cloud_name: Optional[str] = None, cloud_id: Optional[str] = None,
    ) -> str:
        """Get a cloud's current JSON configuration."""

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        return str(get_cloud_json_from_id(cloud_id, self.api_client)["config"])

    def set_default_cloud(
        self, cloud_name: Optional[str], cloud_id: Optional[str],
    ) -> None:
        """
        Sets default cloud for caller's organization. This operation can only be performed
        by organization admins, and the default cloud must have organization level
        permissions.
        """

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        self.api_client.update_default_cloud_api_v2_organizations_update_default_cloud_post(
            cloud_id=cloud_id
        )

        self.log.info(f"Updated default cloud to {cloud_name}")

    def experimental_setup_secrets(
        self,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        write_permissions: bool,
        yes: bool,
    ):
        """
        Given a cloud name, look up its provider and give it permissions to read secrets
        """
        feature_flag_on = self.api_client.check_is_feature_flag_on_api_v2_userinfo_check_is_feature_flag_on_get(
            "wandb-integration-prototype"
        ).result.is_on
        if not feature_flag_on:
            raise ClickException(
                "Secrets can only be set up if the feature flag is enabled. "
                "Please contact Anyscale support to enable the flag."
            )

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )
        cloud = self.api_client.get_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_get(
            cloud_id
        ).result

        self.log.info(
            f"Setting up secrets policy for {cloud.provider} cloud {cloud.name}"
        )

        if cloud.provider == "AWS":
            return self._experimental_grant_secrets_access_aws(
                cloud, write_permissions, yes
            )

        if cloud.provider == "GCP":
            return self._experimental_grant_secrets_access_gcp(
                cloud, write_permissions, yes
            )

        raise ClickException(f"Cloud secrets not supported for {cloud_name}")

    def _experimental_grant_secrets_access_aws(
        self, cloud: CloudWithCloudResource, write_permissions: bool, yes: bool
    ) -> None:
        """Creates IAM policy for SSM readonly access and attaches it to the given role
        Args:
            cloud (Cloud): Cloud object which needs modification
            write_permissions (bool): Whether to add write permissions for Secrets Manager
                to policy
        """

        # Ensure they are in the correct AWS account, by checking account used
        # for Security Token Service
        current_account = get_user_env_aws_account(cloud.region)
        # Cloud credentials of format arn:aws:iam::{cloud_account}:role/{cloud_role}
        # Split credentials to get cloud account.
        cloud_account = cloud.credentials.split(":")[4]

        if current_account != cloud_account:
            raise ClickException(
                f"The cloud you specified uses AWS account {cloud_account}, "
                f"but you are currently logged into {current_account}."
            )

        default_instance_role_name = get_dataplane_role_arn(
            cloud_account, cloud.cloud_resource
        ).to_role_name()
        if yes:
            role_name = default_instance_role_name
        else:
            role_name = prompt(
                "Which AWS role do you want to grant readonly SSM access to?",
                default=default_instance_role_name,
                show_default=True,
            )

        role: Any = _get_role(role_name, cloud.region)
        assert (
            role is not None
        ), f"Failed to find IAM role {role_name} in Cloud {cloud.name}! Have you run 'cloud setup'?"

        policy_name = (
            f"anyscale-secrets-read-write-{cloud.id}"
            if write_permissions
            else f"anyscale-secrets-readonly-{cloud.id}"
        )
        policy_document = (
            ANYSCALE_SSM_READ_WRITE_ACCESS_POLICY_DOCUMENT
            if write_permissions
            else ANYSCALE_SSM_READONLY_ACCESS_POLICY_DOCUMENT
        )

        role.Policy(name=policy_name).put(PolicyDocument=json.dumps(policy_document),)
        self.log.info(
            f"Successfully added/updated inline policy {policy_name} on role {role_name}."
        )

        if role_name == DEFAULT_RAY_IAM_ROLE:
            self.log.info(
                f"Note: {role_name} is the default role used for all Anyscale clouds in "
                f"this AWS account, so policy {policy_name} will be used by all clouds "
                "that use this role. We are planning to create a new default role for each "
                "Anyscale cloud in the future."
            )

    def _experimental_grant_secrets_access_gcp(
        self, cloud: CloudWithCloudResource, write_permissions: bool, yes: bool
    ) -> None:
        from anyscale.utils.gcp_utils import get_application_default_credentials

        (
            credentials,
            default_credentials_project_name,
        ) = get_application_default_credentials(self.log)

        anyscale_cloud_project_name = json.loads(cloud.credentials)["project_id"]
        project_name = default_credentials_project_name or anyscale_cloud_project_name
        if not yes:
            if default_credentials_project_name == anyscale_cloud_project_name:
                prompt_str = (
                    "Your current GCloud credentials and the GCP Project associated "
                    f"with Anyscale Cloud {cloud.name} are for {default_credentials_project_name}"
                )
            else:
                prompt_str = (
                    "Your current GCloud credentials "
                    + (
                        f"are for project {default_credentials_project_name}."
                        if default_credentials_project_name
                        else "do not contain a project."
                    )
                    + f"\nThe GCP Project associated with Anyscale Cloud {cloud.name} is {anyscale_cloud_project_name}."
                )
            project_name = prompt(
                (f"{prompt_str}\nWhich project are you using to store secrets?"),
                default=project_name,
            )

        discovery = try_import_gcp_discovery()
        projects_client = discovery.build(
            "cloudresourcemanager", "v3", credentials=credentials
        ).projects()
        current_policy = projects_client.getIamPolicy(
            resource=f"projects/{project_name}"
        ).execute()

        svc_account = "{}@{}".format(
            cloud.id.replace("_", "-").lower(),
            json.loads(cloud.credentials)["service_account_email"].split("@")[1],
        )

        if not yes:
            svc_account = prompt(
                "Which service account do you want to grant Secrets Manager access to?\n"
                "This defaults to the cloud-specific service account for this cloud",
                default=svc_account,
            )

        if write_permissions:
            current_policy["bindings"].extend(
                [
                    # Granting secretmanager.admin permissions to instance because it is
                    # the only role which supports creating a secret.
                    {
                        "role": "roles/secretmanager.admin",
                        "members": f"serviceAccount:{svc_account}",
                    },
                ]
            )
        else:
            current_policy["bindings"].extend(
                [
                    {
                        "role": "roles/secretmanager.viewer",
                        "members": f"serviceAccount:{svc_account}",
                    },
                    {
                        "role": "roles/secretmanager.secretAccessor",
                        "members": f"serviceAccount:{svc_account}",
                    },
                ]
            )

        projects_client.setIamPolicy(
            resource=f"projects/{project_name}", body={"policy": current_policy}
        ).execute()

        self.log.info(
            f"Successfully updated the IAM policy for projects/{project_name}."
        )

        serviceusage_resource = discovery.build(
            "serviceusage", "v1", credentials=credentials
        )
        api_state = (
            serviceusage_resource.services()
            .get(name=f"projects/{project_name}/services/secretmanager.googleapis.com")
            .execute()
        )
        if api_state["state"] != "ENABLED":
            if not yes and not click.confirm(
                f"The project projects/{project_name} doesn't have the Secret Manager "
                "API enabled. Do you want to enable it?"
            ):
                return

            (
                serviceusage_resource.services()
                .enable(
                    name=f"projects/{project_name}/services/secretmanager.googleapis.com"
                )
                .execute()
            )
            self.log.info(
                f"Enabled Secret Manager API for projects/{project_name}. This operation "
                "may take a few minutes for the API to be ready."
            )

    def _passed_or_failed_str_from_bool(self, is_passing: bool) -> str:
        return "PASSED" if is_passing else "FAILED"

    def verify_cloud(
        self,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        boto3_session: Optional[Any] = None,
        strict: bool = False,
    ) -> bool:
        """
        Verifies a cloud by name or id.
        """
        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        cloud = self.api_client.get_cloud_api_v2_clouds_cloud_id_get(cloud_id).result

        if cloud.state == CloudState.DELETING or cloud.state == CloudState.DELETED:
            self.log.info(
                f"This cloud {cloud_name}({cloud_id}) is either during deletion or deleted. Skipping verification."
            )
            return False

        cloud_resource = get_cloud_resource_by_cloud_id(
            cloud_id, cloud.provider, self.api_client
        )
        if cloud_resource is None:
            self.log.error(
                f"This cloud {cloud_name}({cloud_id}) does not contain resource records."
            )
            return False

        if cloud.provider == "AWS":
            if boto3_session is None:
                boto3_session = boto3.Session(region_name=cloud.region)
            return self.verify_aws_cloud_resources(
                cloud_resource=cloud_resource,
                boto3_session=boto3_session,
                region=cloud.region,
                cloud_id=cloud_id,
                is_bring_your_own_resource=cloud.is_bring_your_own_resource,
                is_private_network=cloud.is_private_cloud
                if cloud.is_private_cloud
                else False,
                strict=strict,
            )
        elif cloud.provider == "GCP":
            project_id = json.loads(cloud.credentials)["project_id"]
            return self.verify_gcp_cloud_resources(
                cloud_resource=cloud_resource,
                project_id=project_id,
                region=cloud.region,
                cloud_id=cloud_id,
                yes=False,
                strict=strict,
            )
        else:
            self.log.error(
                f"This cloud {cloud_name}({cloud_id}) does not have a valid cloud provider."
            )
            return False

    def verify_aws_cloud_resources(
        self,
        *,
        cloud_resource: CreateCloudResource,
        boto3_session: boto3.Session,
        region: str,
        is_private_network: bool,
        cloud_id: str,
        is_bring_your_own_resource: bool = False,
        ignore_capacity_errors: bool = IGNORE_CAPACITY_ERRORS,
        logger: BlockLogger = None,
        strict: bool = False,
    ):
        if not logger:
            logger = self.log

        verify_aws_vpc_result = verify_aws_vpc(
            cloud_resource=cloud_resource,
            boto3_session=boto3_session,
            logger=logger,
            ignore_capacity_errors=ignore_capacity_errors,
            strict=strict,
        )
        verify_aws_subnets_result = verify_aws_subnets(
            cloud_resource=cloud_resource,
            region=region,
            logger=logger,
            ignore_capacity_errors=ignore_capacity_errors,
            is_private_network=is_private_network,
            strict=strict,
        )

        anyscale_aws_account = (
            self.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get().result.anyscale_aws_account
        )
        verify_aws_iam_roles_result = verify_aws_iam_roles(
            cloud_resource=cloud_resource,
            boto3_session=boto3_session,
            anyscale_aws_account=anyscale_aws_account,
            logger=logger,
            strict=strict,
        )
        verify_aws_security_groups_result = verify_aws_security_groups(
            cloud_resource=cloud_resource,
            boto3_session=boto3_session,
            logger=self.log,
            strict=strict,
        )
        verify_aws_s3_result = verify_aws_s3(
            cloud_resource=cloud_resource,
            boto3_session=boto3_session,
            region=region,
            logger=logger,
            strict=strict,
        )
        verify_aws_efs_result = verify_aws_efs(
            cloud_resource=cloud_resource,
            boto3_session=boto3_session,
            logger=logger,
            strict=strict,
        )
        # Cloudformation is only used in managed cloud setup. Set to True in BYOR case because it's not used.
        verify_aws_cloudformation_stack_result = True
        if not is_bring_your_own_resource:
            verify_aws_cloudformation_stack_result = verify_aws_cloudformation_stack(
                cloud_resource=cloud_resource,
                boto3_session=boto3_session,
                logger=logger,
                strict=strict,
            )

        verify_anyscale_access_result = verify_anyscale_access(
            self.api_client, cloud_id, logger
        )

        logger.info(
            "\n".join(
                [
                    "Verification result:",
                    f"anyscale access: {self._passed_or_failed_str_from_bool(verify_anyscale_access_result)}",
                    f"vpc: {self._passed_or_failed_str_from_bool(verify_aws_vpc_result)}",
                    f"subnets: {self._passed_or_failed_str_from_bool(verify_aws_subnets_result)}",
                    f"iam roles: {self._passed_or_failed_str_from_bool(verify_aws_iam_roles_result)}",
                    f"security groups: {self._passed_or_failed_str_from_bool(verify_aws_security_groups_result)}",
                    f"s3: {self._passed_or_failed_str_from_bool(verify_aws_s3_result)}",
                    f"efs: {self._passed_or_failed_str_from_bool(verify_aws_efs_result)}",
                    f"cloudformation stack: {self._passed_or_failed_str_from_bool(verify_aws_cloudformation_stack_result) if not is_bring_your_own_resource else 'N/A'}",
                ]
            )
        )

        return all(
            [
                verify_anyscale_access_result,
                verify_aws_vpc_result,
                verify_aws_subnets_result,
                verify_aws_iam_roles_result,
                verify_aws_security_groups_result,
                verify_aws_s3_result,
                verify_aws_efs_result,
                verify_aws_cloudformation_stack_result
                if not is_bring_your_own_resource
                else True,
            ]
        )

    def register_aws_cloud(  # noqa: PLR0913
        self,
        region: str,
        name: str,
        vpc_id: str,
        subnet_ids: List[str],
        efs_id: str,
        anyscale_iam_role_id: str,
        instance_iam_role_id: str,
        security_group_ids: List[str],
        s3_bucket_id: str,
        private_network: bool,
        cluster_management_stack_version: ClusterManagementStackVersions,
        yes: bool = False,
    ):
        # Create a cloud without cloud resources first
        try:
            created_cloud = self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    provider="AWS",
                    region=region,
                    credentials=anyscale_iam_role_id,
                    name=name,
                    is_bring_your_own_resource=True,
                    is_private_cloud=private_network,
                    cluster_management_stack_version=cluster_management_stack_version,
                )
            )
            cloud_id = created_cloud.result.id
        except ClickException as e:
            if "409" in e.message:
                raise ClickException(
                    f"Cloud with name {name} already exists. Please choose a different name."
                )
            raise

        try:
            # Update anyscale IAM role's assume policy to include the cloud id as the external ID
            role = _get_role(
                AwsRoleArn.from_string(anyscale_iam_role_id).to_role_name(), region
            )
            assert (
                role is not None
            ), f"Failed to access IAM role {anyscale_iam_role_id}."
            new_policy = _update_external_ids_for_policy(
                role.assume_role_policy_document, cloud_id  # type: ignore
            )
            role.AssumeRolePolicy().update(PolicyDocument=json.dumps(new_policy))  # type: ignore

            boto3_session = boto3.Session(region_name=region)
            aws_efs_mount_target_ip = _get_aws_efs_mount_target_ip(
                boto3_session, efs_id
            )

            aws_subnet_ids_with_availability_zones = associate_aws_subnets_with_azs(
                subnet_ids, region
            )

            # Verify cloud resources meet our requirement
            create_cloud_resource = CreateCloudResource(
                aws_vpc_id=vpc_id,
                aws_subnet_ids_with_availability_zones=aws_subnet_ids_with_availability_zones,
                aws_iam_role_arns=[anyscale_iam_role_id, instance_iam_role_id],
                aws_security_groups=security_group_ids,
                aws_s3_id=s3_bucket_id,
                aws_efs_id=efs_id,
                aws_efs_mount_target_ip=aws_efs_mount_target_ip,
            )
            with self.log.spinner("Verifying cloud resources...") as spinner:
                if not self.verify_aws_cloud_resources(
                    cloud_resource=create_cloud_resource,
                    boto3_session=boto3_session,
                    region=region,
                    is_bring_your_own_resource=True,
                    is_private_network=private_network,
                    cloud_id=cloud_id,
                    logger=BlockLogger(spinner_manager=spinner),
                ):
                    raise ClickException(
                        "Please make sure all the resources provided meet the requirements and try again."
                    )

            confirm(
                "Please review the output from verification for any warnings. Would you like to proceed with cloud creation?",
                yes,
            )

            # update cloud with verified cloud resources
            self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put(
                cloud_id=cloud_id,
                update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
                    cloud_resource_to_update=create_cloud_resource,
                ),
            )
            self.wait_for_cloud_to_be_active(cloud_id)
        except Exception as e:  # noqa: BLE001
            # Delete the cloud if registering the cloud fails
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )
            raise ClickException(f"Cloud registration failed! {e}")

        self.log.info(f"Successfully created cloud {name}, and it's ready to use.")

    def verify_gcp_cloud_resources(
        self,
        *,
        cloud_resource: CreateCloudResourceGCP,
        project_id: str,
        region: str,
        cloud_id: str,
        yes: bool,
        factory: Any = None,
        strict: bool = False,
    ) -> bool:
        gcp_utils = try_import_gcp_utils()
        if not factory:
            factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)
        GCPLogger = gcp_utils.GCPLogger
        verify_lib = try_import_gcp_verify_lib()

        with self.log.spinner("Verifying cloud resources...") as spinner:
            gcp_logger = GCPLogger(self.log, project_id, spinner, yes)
            verify_gcp_project_result = verify_lib.verify_gcp_project(
                factory, project_id, gcp_logger, strict=strict
            )
            verify_gcp_access_service_account_result = verify_lib.verify_gcp_access_service_account(
                factory, cloud_resource, project_id, gcp_logger
            )
            verify_gcp_dataplane_service_account_result = verify_lib.verify_gcp_dataplane_service_account(
                factory, cloud_resource, project_id, gcp_logger, strict=strict
            )
            verify_gcp_networking_result = verify_lib.verify_gcp_networking(
                factory, cloud_resource, project_id, region, gcp_logger, strict=strict,
            )
            verify_firewall_policy_result = verify_lib.verify_firewall_policy(
                factory, cloud_resource, project_id, region, gcp_logger, strict=strict,
            )
            verify_filestore_result = verify_lib.verify_filestore(
                factory, cloud_resource, region, gcp_logger, strict=strict
            )
            verify_cloud_storage_result = verify_lib.verify_cloud_storage(
                factory, cloud_resource, project_id, region, gcp_logger, strict=strict,
            )
            verify_anyscale_access_result = verify_anyscale_access(
                self.api_client, cloud_id, self.log
            )

        self.log.info(
            "\n".join(
                [
                    "Verification result:",
                    f"anyscale access: {self._passed_or_failed_str_from_bool(verify_anyscale_access_result)}",
                    f"project: {self._passed_or_failed_str_from_bool(verify_gcp_project_result)}",
                    f"vpc and subnet: {self._passed_or_failed_str_from_bool(verify_gcp_networking_result)}",
                    f"anyscale iam service account: {self._passed_or_failed_str_from_bool(verify_gcp_access_service_account_result)}",
                    f"cluster node service account: {self._passed_or_failed_str_from_bool(verify_gcp_dataplane_service_account_result)}",
                    f"firewall policy: {self._passed_or_failed_str_from_bool(verify_firewall_policy_result)}",
                    f"filestore: {self._passed_or_failed_str_from_bool(verify_filestore_result)}",
                    f"cloud storage: {self._passed_or_failed_str_from_bool(verify_cloud_storage_result)}",
                ]
            )
        )

        return all(
            [
                verify_anyscale_access_result,
                verify_gcp_project_result,
                verify_gcp_access_service_account_result,
                verify_gcp_dataplane_service_account_result,
                verify_gcp_networking_result,
                verify_firewall_policy_result,
                verify_filestore_result,
                verify_cloud_storage_result,
            ]
        )

    def register_gcp_cloud(  # noqa: PLR0913
        self,
        region: str,
        name: str,
        project_id: str,
        vpc_name: str,
        subnet_names: List[str],
        filestore_instance_id: str,
        filestore_location: str,
        anyscale_service_account_email: str,
        instance_service_account_email: str,
        provider_id: str,
        firewall_policy_names: List[str],
        cloud_storage_bucket_name: str,
        private_network: bool,
        cluster_management_stack_version: ClusterManagementStackVersions,
        yes: bool = False,
    ):
        gcp_utils = try_import_gcp_utils()

        # Create a cloud without cloud resources first
        assert re.search(
            "projects/[0-9]*/locations/global/workloadIdentityPools/.+/providers/.+",
            provider_id,
        ), f"Invalid provider_id {provider_id}"
        try:
            credentials = json.dumps(
                {
                    "project_id": project_id,
                    "provider_id": provider_id,
                    "service_account_email": anyscale_service_account_email,
                }
            )

            created_cloud = self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    provider="GCP",
                    region=region,
                    credentials=credentials,
                    name=name,
                    is_bring_your_own_resource=True,
                    is_private_cloud=private_network,
                    cluster_management_stack_version=cluster_management_stack_version,
                )
            )
            cloud_id = created_cloud.result.id
        except ClickException as e:
            if "409" in e.message:
                raise ClickException(
                    f"Cloud with name {name} already exists. Please choose a different name."
                )
            raise

        try:
            factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)

            filestore_config = gcp_utils.get_gcp_filestore_config(
                factory,
                project_id,
                vpc_name,
                filestore_location,
                filestore_instance_id,
                self.log,
            )

            # Verify cloud resources meet our requirement
            create_cloud_resource_gcp = CreateCloudResourceGCP(
                gcp_vpc_id=vpc_name,
                gcp_subnet_ids=subnet_names,
                gcp_cluster_node_service_account_email=instance_service_account_email,
                gcp_anyscale_iam_service_account_email=anyscale_service_account_email,
                gcp_filestore_config=filestore_config,
                gcp_firewall_policy_ids=firewall_policy_names,
                gcp_cloud_storage_bucket_id=cloud_storage_bucket_name,
            )

            if not self.verify_gcp_cloud_resources(
                cloud_resource=create_cloud_resource_gcp,
                project_id=project_id,
                region=region,
                cloud_id=cloud_id,
                yes=yes,
                factory=factory,
            ):
                raise ClickException(
                    "Please make sure all the resources provided meet the requirements and try again."
                )

            confirm(
                "Please review the output from verification for any warnings. Would you like to proceed with cloud creation?",
                yes,
            )

            # update cloud with verified cloud resources
            self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_put(
                cloud_id=cloud_id,
                update_cloud_with_cloud_resource_gcp=UpdateCloudWithCloudResourceGCP(
                    cloud_resource_to_update=create_cloud_resource_gcp,
                ),
            )
            self.wait_for_cloud_to_be_active(cloud_id)
        except Exception as e:  # noqa: BLE001
            # Delete the cloud if registering the cloud fails
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )
            raise ClickException(f"Cloud registration failed! {e}")

        self.log.info(f"Successfully created cloud {name}, and it's ready to use.")

    def delete_cloud(
        self,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        skip_confirmation: bool,
    ) -> bool:
        """
        Deletes a cloud by name or id.
        """

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        try:
            response = self.api_client.get_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_get(
                cloud_id=cloud_id
            )
            cloud = response.result
        except ClickException as e:
            self.log.error(e)
            raise ClickException(f"Failed to get cloud with name {cloud_name}.")

        confirmation_msg = f"\nIf the cloud {cloud_id} is deleted, you will not be able to access existing clusters of this cloud.\n"
        if cloud.is_bring_your_own_resource:
            confirmation_msg += "Note that Anyscale does not delete any of the cloud provider resources created by you.\n"

        confirm(
            f"{confirmation_msg}\nFor more information, please refer to the documentation https://docs.anyscale.com/user-guide/onboard/clouds/deploy-on-aws#delete-an-anyscale-cloud\nContinue?",
            skip_confirmation,
        )

        try:
            response = self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put(
                cloud_id=cloud_id,
                update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
                    state=CloudState.DELETING
                ),
            )
            cloud = response.result
        except ClickException as e:
            self.log.error(e)
            raise ClickException(
                f"Failed to update cloud state to deleting for cloud {cloud_name}."
            )

        if (
            cloud.provider.lower() == "aws"
            and cloud.is_bring_your_own_resource is False
        ):
            try:
                self.delete_aws_managed_cloud(cloud=cloud)
            except ClickException as e:
                confirm(
                    f"Error while trying to clean up AWS resources:\n{e}\n"
                    "Do you want to force delete this cloud? You will need to clean up any associated resources on your own.\n"
                    "Continue with force deletion?",
                    skip_confirmation,
                )

        elif cloud.provider.lower() == "aws" and not cloud.is_k8s and not cloud.is_aioa:
            self.log.warning(
                f"The trust policy that allows Anyscale to assume {cloud.credentials} is still in place. Please delete it manually if you no longer wish anyscale to have access."
            )
        try:
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )
        except ClickException as e:
            self.log.error(e)
            raise ClickException(f"Failed to delete cloud with name {cloud_name}.")

        self.log.info(f"Deleted cloud with name {cloud_name}.")
        return True

    def delete_aws_managed_cloud(self, cloud: CloudWithCloudResource) -> bool:
        if (
            not cloud.cloud_resource
            or not cloud.cloud_resource.aws_cloudformation_stack_id
        ):
            raise ClickException(
                f"This cloud {cloud.id} does not have a cloudformation stack."
            )

        cfn_client = _client("cloudformation", cloud.region)
        cfn_stack_arn = cloud.cloud_resource.aws_cloudformation_stack_id
        cfn_stack_url = f"https://{cloud.region}.console.aws.amazon.com/cloudformation/home?region={cloud.region}#/stacks/stackinfo?stackId={cfn_stack_arn}"
        try:
            cfn_client.delete_stack(StackName=cfn_stack_arn)
        except ClientError:
            raise ClickException(
                f"Failed to delete cloudformation stack {cfn_stack_arn}.\nPlease view it at {cfn_stack_url}"
            ) from None

        self.log.info(f"\nTrack progress of cloudformation at {cfn_stack_url}")
        with self.log.spinner("Deleting cloud resources through cloudformation..."):
            end_time = time.time() + CLOUDFORMATION_TIMEOUT_SECONDS
            while time.time() < end_time:
                try:
                    cfn_stack = cfn_client.describe_stacks(StackName=cfn_stack_arn)[
                        "Stacks"
                    ][0]
                except ClientError as e:
                    raise ClickException(
                        f"Failed to fetch the cloudformation stack {cfn_stack_arn}. Please check you have the right AWS credentials and the cloudformation stack still exists. Error details: {e}"
                    ) from None

                if cfn_stack["StackStatus"] == "DELETE_COMPLETE":
                    self.log.info(
                        f"Cloudformation stack {cfn_stack['StackId']} is deleted."
                    )
                    break

                if cfn_stack["StackStatus"] in ("DELETE_FAILED",):
                    # Provide link to cloudformation
                    raise ClickException(
                        f"Failed to delete cloud resources. Please check your cloudformation stack for errors. {cfn_stack_url}"
                    )
                time.sleep(1)

            if time.time() > end_time:
                raise ClickException(
                    f"Timed out deleting AWS resources. Please check your cloudformation stack for errors. {cfn_stack['StackId']}"
                )
        self.log.info(
            f"\nThe S3 bucket ({cloud.cloud_resource.aws_s3_id}) associated with this cloud still exists."
            "\nIf you no longer need the data associated with this bucket, please delete it."
        )
        return True
