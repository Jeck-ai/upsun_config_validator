# schema.py
import re
import os
import json

# @todo: periodically grab these versions from platformsh/platformsh-docs.
registryLocation = "{0}/{1}".format(os.path.dirname(os.path.abspath(__file__)), "/data/registry.json")
ALLOWED_VERSIONS = {}
with open(registryLocation) as json_data:
    data = json.load(json_data)
    for key in data:
        ALLOWED_VERSIONS[key] = {
            "type": key,
            "runtime": data[key]["runtime"],
            "versions": data[key]["versions"]["supported"],
        }
        if "disk" in data[key]:
            ALLOWED_VERSIONS[key]["disk"] = data[key]["disk"]
        if "endpoint" in data[key]:
            ALLOWED_VERSIONS[key]["endpoint"] = data[key]["endpoint"]
        if "min_disk_size" in data[key]:
            ALLOWED_VERSIONS[key]["min_disk_size"] = data[key]["min_disk_size"]

def validate_runtime_version(runtime_type):
    """
    Validate runtime type and version format
    
    Validates:
    1. Uses ':' separator
    2. Runtime type is supported
    3. Version is valid for that runtime
    """
    # Regex to parse runtime:version
    match = re.match(r'^([\w-]+):(.+)$', runtime_type)
    
    if not match:
        return False, f"Invalid runtime type format. Must use ':' separator in '{runtime_type}'"
    
    runtime, version = match.groups()
    
    # Check if runtime is supported
    if runtime not in ALLOWED_VERSIONS:
        return False, f"Unsupported runtime type '{runtime}'. Supported runtimes are: {', '.join(ALLOWED_VERSIONS.keys())}"
    
    # Check version format and allowed versions
    valid_versions = ALLOWED_VERSIONS[runtime]["versions"]
    
    # Support exact version match or x-based versions
    if version == 'x' or version.endswith('.x'):
        # Remove .x to check major version
        version_base = version.rstrip('.x')
        if any(v.startswith(version_base) for v in valid_versions):
            return True, None
    
    # Exact version match
    if version in valid_versions:
        return True, None
    
    return False, f"Unsupported version '{version}' for runtime '{runtime}'. Allowed versions are: {', '.join(valid_versions)}"

UPSUN_SCHEMA = {
    "type": "object",
    "properties": {
        "applications": {
            "type": "object",
            "minProperties": 1,
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "pattern": "^(nodejs|php|python|golang|ruby|java|dotnet|static|clojure|elixir|perl|sbcl|perlcgi|phpcgi|rust|bun)[@:][0-9]+(\\.[0-9]+)*$",
                        "x-runtime-validator": validate_runtime_version
                    },
                    # Rest of the schema remains the same
                    "stack": {
                        "type": "array",
                        "items": {
                            "oneOf": [
                                {"type": "string"},
                                {
                                    "type": "object",
                                    "properties": {
                                        "extensions": {"type": "array", "items": {"type": "string"}},
                                        "version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+(\\.[0-9]+)?$"}
                                    }
                                }
                            ]
                        }
                    },
                    # ... rest of the properties ...
                },
                "oneOf": [
                    {"required": ["type"]},
                    {"required": ["stack"]}
                ],
                "additionalProperties": False
            }
        },
        # Rest of the schema remains the same ...
        "services": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "pattern": "^(mariadb|mysql|oracle-mysql|postgresql|redis|memcached|rabbitmq|solr|elasticsearch|mongodb|mongodb-enterprise|influxdb|kafka|varnish|opensearch):[0-9]+(\\.[0-9]+)*$"
                    },
                    # ... rest of the services properties ...
                },
                "required": ["type"],
                "additionalProperties": False
            }
        },
        # ... rest of the schema remains the same ...
    },
    "required": ["applications"],
    "additionalProperties": False
}