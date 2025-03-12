import os
import glob

def load_yaml_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def get_yaml_files(directory):
    yaml_files = {}
    for file in glob.glob(f"{directory}/**/*.yaml", recursive=True, include_hidden=True):
        if ".upsun" in file:
            if "upsun" not in yaml_files:
                yaml_files["upsun"] = [file]
            else: 
                yaml_files["upsun"].append(file)
        if (".platform" in file) or (".platform.app.yaml" in file):
            if "platformsh" not in yaml_files:
                yaml_files["platformsh"] = [file]
            else: 
                yaml_files["platformsh"].append(file)
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


def make_bold_text(text):
        bold = ["\033[1m", "\033[0m"]
        return f"\n{bold[0]}{text}{bold[1]}\n"