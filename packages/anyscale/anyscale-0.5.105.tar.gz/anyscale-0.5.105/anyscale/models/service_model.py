import enum
from typing import Any, Dict, Optional

import click
from pydantic import Field, root_validator

from anyscale.controllers.job_controller import (
    _validate_conda_option,
    _validate_env_vars,
    _validate_pip_option,
    _validate_py_modules,
    _validate_upload_path,
    _validate_working_dir,
    _validate_working_dir_and_upload_path,
    BaseHAJobConfig,
)


class UserServiceAccessTypes(str, enum.Enum):
    private = "private"
    public = "public"


class ServiceConfig(BaseHAJobConfig):

    healthcheck_url: Optional[str] = Field(
        None, description="Healthcheck url for service."
    )
    access: UserServiceAccessTypes = Field(
        UserServiceAccessTypes.public,
        description=(
            "Whether user service (eg: serve deployment) can be accessed by public "
            "internet traffic. If public, a user service endpoint can be queried from "
            "the public internet with the provided authentication token. "
            "If private, the user service endpoint can only be queried from within "
            "the same Anyscale cloud and will not require an authentication token."
        ),
    )

    entrypoint: Optional[str] = Field(
        None,
        description="A script that will be run to start your job. This command will be run in the root directory of the specified runtime env. Eg. 'python script.py'",
    )

    ray_serve_config: Optional[Dict[str, Any]] = Field(
        None,
        description=(
            "The Ray Serve config to use for this Production service. It is supported only on v2 clouds. "
            "This config defines your Ray Serve application, and will be passed directly to Ray Serve. "
            "You can learn more about Ray Serve config files here: https://docs.ray.io/en/latest/serve/production-guide/config.html"
        ),
    )

    ray_gcs_external_storage_config: Optional[Dict[str, Any]] = Field(
        None,
        description=(
            "Address to connect to external storage at. "
            "Must be accessible from instances running in the provided cloud. "
            "This is only supported for v2 services."
        ),
    )

    # Version level fields for Services V2
    version: Optional[str] = Field(
        None,
        description="A version string that represents the version for this service. "
        "Will be populated with the hash of the config if not specified.",
    )
    canary_percent: Optional[int] = Field(
        None,
        description="A manual target weight for this service. "
        "If this field is not set, the service will automatically roll out. "
        "If set, this should be a number between 0 and 100 (inclusive). "
        "The newly created version will have weight `canary_percent` "
        "and the existing version will have `100 - canary_percent`.",
    )

    rollout_strategy: Optional[str] = Field(
        None,
        description="Strategy for rollout. "
        "The ROLLOUT strategy will deploy your Ray Serve configuration onto a newly started cluster, and then shift traffic over to the new cluster. "
        "You can manually control the speed of the rollout using the canary_weight configuration.\n"
        "The IN_PLACE strategy will use Ray Serve in place upgrade to update your existing cluster in place. "
        "When using this rollout strategy, you may only change the ray_serve_config field. "
        "You cannot partially shift traffic or rollback an in place upgrade. "
        "In place upgrades are faster and riskier than rollouts, and we recommend only using them for relatively safe changes (for example, increasing the number of replicas on a Ray Serve deployment).\n"
        "Default strategy is ROLLOUT.",
    )

    @root_validator
    def validates_config(cls, values) -> Dict[str, Any]:
        # entrypoint is used for Services V1 and serve config for Services V2
        is_entrypoint_present = bool(values.get("entrypoint"))
        is_serve_config_present = bool(values.get("ray_serve_config"))
        assert is_entrypoint_present != is_serve_config_present, (
            "Please specify one of 'entrypoint' or 'ray_serve_config'. "
            "'entrypoint' should be specified on v1 clouds, "
            "and 'ray_serve_config' should be specified on v2 clouds."
        )

        if is_entrypoint_present:
            assert (
                values.get("healthcheck_url") is not None
            ), "healthcheck_url should be set for Services on v1 clouds."
        if is_serve_config_present:
            assert (
                values.get("healthcheck_url") is None
            ), "healthcheck_url should not be set for Services on v2 clouds."
            assert (
                values.get("runtime_env") is None
            ), "runtime_env should not be set for Services on v2 clouds."

        return values

    @root_validator
    def validate_runtime_env_v2(cls: Any, values: Any) -> Any:  # noqa: PLR0912
        ray_serve_config = values.get("ray_serve_config")
        if ray_serve_config:
            runtime_env = ray_serve_config.get("runtime_env")
            if runtime_env is not None:
                if "conda" in runtime_env:
                    conda_option = runtime_env["conda"]
                    if not isinstance(conda_option, (str, dict)):
                        raise click.ClickException(
                            f"runtime_env['conda'] must be str or dict, got type({conda_option})."
                        )
                    runtime_env["conda"] = _validate_conda_option(conda_option)
                if "pip" in runtime_env:
                    pip_option = runtime_env["pip"]
                    if not isinstance(pip_option, (str, list)):
                        raise click.ClickException(
                            f"runtime_env['pip'] must be str or list, got type({pip_option})."
                        )
                    runtime_env["pip"] = _validate_pip_option(runtime_env["pip"])
                if "py_modules" in runtime_env:
                    py_modules_option = runtime_env["py_modules"]
                    if not isinstance(py_modules_option, list):
                        raise click.ClickException(
                            f"runtime_env['py_modules'] must be list, got type({py_modules_option})."
                        )
                    runtime_env["py_modules"] = _validate_py_modules(py_modules_option)
                if "upload_path" in runtime_env:
                    upload_path_option = runtime_env["upload_path"]
                    if not isinstance(upload_path_option, str):
                        raise click.ClickException(
                            f"runtime_env['upload_path'] must be str, got type({upload_path_option})."
                        )
                    runtime_env["upload_path"] = _validate_upload_path(
                        upload_path_option
                    )
                if "working_dir" in runtime_env:
                    working_dir_option = runtime_env["working_dir"]
                    if not isinstance(working_dir_option, str):
                        raise click.ClickException(
                            f"runtime_env['working_dir'] must be str, got type({working_dir_option})."
                        )
                    runtime_env["working_dir"] = _validate_working_dir(
                        working_dir_option
                    )
                _validate_working_dir_and_upload_path(
                    runtime_env.get("working_dir"), runtime_env.get("upload_path")
                )
                if "env_vars" in runtime_env:
                    env_vars_option = runtime_env["env_vars"]
                    if not isinstance(env_vars_option, dict):
                        raise click.ClickException(
                            f"runtime_env['env_vars'] must be dict, got type({env_vars_option})."
                        )
                    runtime_env["env_vars"] = _validate_env_vars(env_vars_option)
                values["ray_serve_config"]["runtime_env"] = runtime_env

        return values
