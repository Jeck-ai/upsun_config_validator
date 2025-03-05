import os

def load_yaml_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def get_yaml_files(directory):
    yaml_files = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml'):
                if "files/.upsun" in os.path.join(root, file):
                    if "upsun" not in yaml_files:
                        yaml_files["upsun"] = [os.path.join(root, file)]
                    else: 
                        yaml_files["upsun"].append(os.path.join(root, file))
                if "files/.platform" in os.path.join(root, file):
                    if "platformsh" not in yaml_files:
                        yaml_files["platformsh"] = [os.path.join(root, file)]
                    else: 
                        yaml_files["platformsh"].append(os.path.join(root, file))
    return yaml_files

def flatten_validation_error(error):
    error_path = " -> ".join(str(path) for path in error.path)
    return {
        'message': error.message,
        'path': error_path,
        'validator': error.validator,
        'validator_value': error.validator_value
    }

def get_all_projects_in_directory(directory, append_subdir):
    return [ f"{f.path}/{append_subdir}" for f in os.scandir(directory) if f.is_dir() ]

    # projects = []
    # for root, dirs, _ in os.walk(directory):
    #     for d in dirs:
    #         projects.append(os.path.join(root, d))
    # return projects