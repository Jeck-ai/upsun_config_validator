from platformvalidator.utils.utils import get_yaml_files
from platformvalidator.validate.upsun import validate_upsun_config
from platformvalidator.validate.platformsh import validate_platformsh_config


def validate_all(directory):
    # Get all yaml files in the directory
    yaml_files = get_yaml_files(directory)
    results = []

    for provider in yaml_files.keys():
        if provider == "upsun":
            print(f"Upsun configuration found. Validating...")
            results.append(validate_upsun_config(yaml_files))
        elif provider == "platformsh":
            print(f"Platform.sh configuration found. Validating...")
            results.append(validate_platformsh_config(yaml_files))
        else:
            print(f"Unknown provider '{provider}'")

    return results
