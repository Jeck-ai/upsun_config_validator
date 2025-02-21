import os
import sys
import json
from pathlib import Path
from validator import validate_upsun_config

testConfig = "{0}/.upsun/config.yaml".format(sys.argv[-1])

with open(testConfig, 'r') as f:
    yaml_content = f.read()
    
errors = validate_upsun_config(yaml_content)
if errors == ["No errors found. YAML is valid."]:
    print("Configuration is valid!")
else:
    print("Validation errors found:")
    for error in errors:
        print(f"- {error}")
