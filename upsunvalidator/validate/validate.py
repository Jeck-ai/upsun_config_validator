from upsunvalidator.utils.utils import get_yaml_files
from upsunvalidator.validate.upsun import validate_upsun_config


def validate_all(directory):
    # Get all yaml files in the directory
    yaml_files = get_yaml_files(directory)
    results = []

    if "upsun" in yaml_files:
        print(f"Upsun configuration found. Validating...")
        results.append(validate_upsun_config(yaml_files))
    else:
        results.append("No Upsun configuration found.")

    return results
