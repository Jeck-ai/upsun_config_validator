from platformvalidator.utils.utils import get_yaml_files
from platformvalidator.validate.upsun import validate_upsun_config


def validate_all(directory):
    # Get all yaml files in the directory
    yaml_files = get_yaml_files(directory)

    for provider in yaml_files.keys():
        if provider == "upsun":
            validate_upsun_config(yaml_files)
        # elif provider == "platformsh":
        #     validate_platformsh_config(yaml_files[provider])
        # else:
        #     print(f"Unknown provider '{provider}'")

    return ["No errors found. YAML is valid."]
