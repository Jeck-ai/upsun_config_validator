import os
import glob

def load_yaml_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def get_yaml_files(directory):
    yaml_files = {}
    # Specifically look for .upsun/config.yaml in our simplified structure
    upsun_config = os.path.join(directory, ".upsun", "config.yaml")
    
    if os.path.exists(upsun_config):
        yaml_files["upsun"] = [upsun_config]
    
    return yaml_files

def flatten_validation_error(error):
    error_path = " -> ".join(str(path) for path in error.path)
    return {
        'message': error.message,
        'path': error_path,
        'validator': error.validator,
        'validator_value': error.validator_value
    }


