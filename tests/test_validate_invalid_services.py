import yaml
import pytest

from upsunvalidator.utils.utils import get_yaml_files
from upsunvalidator.utils.utils import load_yaml_file
from upsunvalidator.utils.utils import get_all_projects_in_directory

from upsunvalidator.validate.upsun import validate_upsun_config
from upsunvalidator.validate.platformsh import validate_platformsh_config
from upsunvalidator.validate.errors import InvalidServiceVersionError

from upsunvalidator.schemas.services import SERVICE_VERSIONS

from .shared import INVALID_RUNTIME_VERSION_DIR
from .shared import INVALID_SERVICE_VERSION_DIR

@pytest.mark.parametrize("current_template", get_all_projects_in_directory(INVALID_RUNTIME_VERSION_DIR, "files"))
def test_invalid_runtime_versions(current_template):
    yaml_files = get_yaml_files(current_template)

    # Upsun applications & services.
    if "upsun" in yaml_files:
        service = current_template.split("/")[-2]
        data = yaml.safe_load(load_yaml_file(yaml_files["upsun"][0]))
        app_name = list(data["applications"].keys())[0]
        invalid_version = data["applications"][app_name]["type"].split(":")[1]
        valid_versions = SERVICE_VERSIONS[service]["versions"]

        msg = f"""

✘ Error found in application '{app_name}':

  Unsupported version '{invalid_version}' for runtime '{service}'. Supported versions are: \n\n    · {'\n    · '.join(valid_versions)}

✔ Recommendation:

  Update your configuration for the runtime '{app_name}' to use one of the supported versions listed above.

  Example:

    ```
    applications:
      {app_name}:
        type: '{service}:{valid_versions[0]}'
    ```
"""

        with pytest.raises(InvalidServiceVersionError, match=msg):
            validate_upsun_config(yaml_files)

    # Platform.sh applications.
    if "platformsh" in yaml_files:
        app_file = [file for file in yaml_files["platformsh"] if ".platform.app.yaml" in file][0]
        service = current_template.split("/")[-2]
        data = yaml.safe_load(load_yaml_file(app_file))
        app_name = data["name"]
        invalid_version = data["type"].split(":")[1]
        valid_versions = SERVICE_VERSIONS[service]["versions"]

        msg = f"""

✘ Error found in application '{app_name}':

  Unsupported version '{invalid_version}' for runtime '{service}'. Supported versions are: \n\n    · {'\n    · '.join(valid_versions)}

✔ Recommendation:

  Update your configuration for the runtime '{app_name}' to use one of the supported versions listed above.

  Example:

    ```
    applications:
      {app_name}:
        type: '{service}:{valid_versions[0]}'
    ```
"""
        with pytest.raises(InvalidServiceVersionError, match=msg):
            validate_platformsh_config(yaml_files)

@pytest.mark.parametrize("current_template", get_all_projects_in_directory(INVALID_SERVICE_VERSION_DIR, "files"))
def test_invalid_service_versions(current_template):
    yaml_files = get_yaml_files(current_template)

    if "upsun" in yaml_files:
        service = current_template.split("/")[-2]
        data = yaml.safe_load(load_yaml_file(yaml_files["upsun"][0]))
        service_name = list(data["services"].keys())[0]
        invalid_version = data["services"][service_name]["type"].split(":")[1]
        valid_versions = SERVICE_VERSIONS[service]["versions"]

        msg = f"""

✘ Error found in service '{service_name}':

  Unsupported version '{invalid_version}' for service '{service}'. Supported versions are: \n\n    · {'\n    · '.join(valid_versions)}

✔ Recommendation:

  Update your configuration for the service '{service_name}' to use one of the supported versions listed above.

  Example:

    ```
    services:
      {service_name}:
        type: '{service}:{valid_versions[0]}'
    ```
"""
        
        with pytest.raises(InvalidServiceVersionError, match=msg):
            validate_upsun_config(yaml_files)

    # Platform.sh services.
    if "platformsh" in yaml_files:
        services_file = [file for file in yaml_files["platformsh"] if ".platform/services.yaml" in file][0]
        service = current_template.split("/")[-2]
        data = yaml.safe_load(load_yaml_file(services_file))
        service_name = list(data.keys())[0]
        invalid_version = data[service_name]["type"].split(":")[1]
        valid_versions = SERVICE_VERSIONS[service]["versions"]

        msg = f"""

✘ Error found in service '{service_name}':

  Unsupported version '{invalid_version}' for service '{service}'. Supported versions are: \n\n    · {'\n    · '.join(valid_versions)}

✔ Recommendation:

  Update your configuration for the service '{service_name}' to use one of the supported versions listed above.

  Example:

    ```
    services:
      {service_name}:
        type: '{service}:{valid_versions[0]}'
    ```
"""
        with pytest.raises(InvalidServiceVersionError, match=msg):
            validate_platformsh_config(yaml_files)
