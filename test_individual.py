import os
import pathlib
import glob
import yaml
import sys
import json
from pathlib import Path
from validator import validate_upsun_config, validate_platformsh_config

print("Validating Upsun Configuration....")

upsunConfig = "{0}/.upsun/config.yaml".format(sys.argv[-1])

with open(upsunConfig, 'r') as f:
    yaml_content = f.read()
    
errors = validate_upsun_config(yaml_content)
if errors == ["No errors found. YAML is valid."]:
    print("Configuration is valid!")
else:
    print("Validation errors found:")
    for error in errors:
        print(f"- {error}")

print("\nValidating Platform.sh Configuration....")

files = [f for f in pathlib.Path(sys.argv[-1]).glob("*.yaml")]
files = files + [f for f in pathlib.Path(sys.argv[-1] + "/.platform/").glob("*.yaml")]

yaml_app_content = ""
yaml_routes_content = ""
yaml_services_content = ""

for file in files:
    with open(file, 'r') as f:
        yaml_content = f.read()
        data = yaml.safe_load(yaml_content)
        if data is not None:
            if "name" in data:
                yaml_app_content = yaml_content
            elif ("https://{default}/" in data) or ("https://{default}" in data):
                yaml_routes_content = yaml_content
            else:
                yaml_services_content = yaml_content
    
errors = validate_platformsh_config(yaml_app_content, yaml_routes_content, yaml_services_content)
if errors == ["No errors found. YAML is valid."]:
    print("Configuration is valid!")
else:
    print("Validation errors found:")
    for error in errors:
        print(f"- {error}")
