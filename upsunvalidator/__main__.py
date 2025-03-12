import os
import yaml
from upsunvalidator.utils.utils import get_yaml_files
from upsunvalidator.validate.upsun import validate_upsun_config, validate_upsun_config_string
from jsonschema import ValidationError

def validate(src=None):
    """Validate a project's Upsun configuration files against schemas.
    
    Args:
        src (str, optional): Repository location to validate. Defaults to current directory.
        
    Returns:
        tuple: (is_valid, message) - Boolean success status and validation message
    """
    if not src:
        src = os.getcwd()

    yaml_files = get_yaml_files(src)
    
    if yaml_files and "upsun" in yaml_files:
        try:
            results = validate_upsun_config(yaml_files)
            return True, results[0]
        except Exception as e:
            return False, str(e)
    else:
        return False, "No Upsun configuration files found."

def validate_string(config_content):
    """Validate a string containing Upsun configuration YAML.
    
    This function is the primary entry point for string-based validation, allowing
    validation of configuration without reading from the filesystem. This is useful
    for:
    
    - Integration with other tools that already have the configuration as a string
    - Validating configurations before they are written to disk
    - Testing configurations from non-file sources (e.g., API responses)
    
    Args:
        config_content (str): String containing YAML configuration
        
    Returns:
        tuple: (is_valid, message) - Boolean success status and validation message
    """
    if not config_content or config_content.strip() == "":
        return False, "YAML parsing error: Empty configuration"
        
    try:
        results = validate_upsun_config_string(config_content)
        return True, results[0]
    except yaml.YAMLError as e:
        return False, f"YAML parsing error: {str(e)}"
    except Exception as e:
        return False, str(e)

if __name__ == '__main__':
    # Simple example usage
    success, message = validate()
    print(message)
