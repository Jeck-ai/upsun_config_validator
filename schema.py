# schema.py
import re

ALLOWED_VERSIONS = {
    "nodejs": ["22", "20", "18", "16"],
    "php": ["8.4", "8.3", "8.2", "8.1"],
    "python": ["3.12", "3.11", "3.10", "3.9", "3.8"],
    "golang": ["1.23", "1.22", "1.21", "1.20", "1.19"],
    "ruby": ["3.3", "3.2", "3.1", "3.0"],
    "java": ["21", "19", "18", "17", "11", "8"],
    "dotnet": ["8.0", "6.0", "7.0"],
    "lisp": ["2.1", "2.0", "1.5"],
    "elixir": ["1.15", "1.14"],
    "rust": ["1"],
    "bun": ["1.0"]
}

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
    valid_versions = ALLOWED_VERSIONS[runtime]
    
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