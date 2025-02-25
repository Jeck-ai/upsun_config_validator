# schema.py
import re
import os
import json

# @todo: GH Action: periodically grab these versions from platformsh/platformsh-docs.
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

        # Duplicate for the `redis-persistent` option
        if key == "redis":
            ALLOWED_VERSIONS["redis-persistent"] = ALLOWED_VERSIONS[key]

def validate_service_version(service_type):
    """
    Validate service type and version format
    
    Validates:
    1. Uses ':' separator
    2. Service type is supported
    3. Version is valid for that service

    @todo: this step does not understand the composable image, which is 1) a subset of services + 2) all of nixpkgs that aren't services - https://docs.upsun.com/create-apps/app-reference/composable-image.html#supported-nix-packages
    """
    # Regex to parse service:version
    match = re.match(r'^([\w-]+):(.+)$', service_type)
    
    if not match:
        return False, f"Invalid service type format. Must use ':' separator in '{service_type}'"
    
    service, version = match.groups()
    
    # Check if run   is supported
    if service not in ALLOWED_VERSIONS:
        return False, f"Unsupported service type '{service}'. Supported services are: {', '.join(ALLOWED_VERSIONS.keys())}"
    
    # Check version format and allowed versions
    valid_versions = ALLOWED_VERSIONS[service]["versions"]
    
    # Support exact version match or x-based versions
    if version == 'x' or version.endswith('.x'):
        # Remove .x to check major version
        version_base = version.rstrip('.x')
        if any(v.startswith(version_base) for v in valid_versions):
            return True, None
    
    # Exact version match
    if version in valid_versions:
        return True, None
    
    return False, f"Unsupported version '{version}' for service '{service}'. Allowed versions are: {', '.join(valid_versions)}"

# UPSUN
upsunSchemaFile = "{0}/{1}".format(os.path.dirname(os.path.abspath(__file__)), "/data/schema/upsun.json")
with open(upsunSchemaFile) as json_data:
    UPSUN_SCHEMA = json.load(json_data)

    # @todo: Some spec overrides, which will need investigation
    UPSUN_SCHEMA["properties"]["applications"]["additionalProperties"]["properties"]["web"]["properties"]["locations"]["additionalProperties"]["properties"]["expires"]["type"] = ["string", "integer"]

# PLATFORMSH
platformshAppSchemaFile = "{0}/{1}".format(os.path.dirname(os.path.abspath(__file__)), "/data/schema/platformsh.application.json")
with open(platformshAppSchemaFile) as json_data:
    PLATFORMSH_SCHEMA_APPS = json.load(json_data)

# @todo: OVERRIDE: Some spec overrides, which will need investigation
# web.locations - default value is -1 (int) for expected type string
PLATFORMSH_SCHEMA_APPS["properties"]["web"]["properties"]["locations"]["additionalProperties"]["properties"]["expires"]["type"] = ["string", "integer"]
UPSUN_SCHEMA["properties"]["applications"]["additionalProperties"]["properties"]["web"]["properties"]["locations"]["additionalProperties"]["properties"]["expires"]["type"] = ["string", "integer"]

platformshRoutesSchemaFile = "{0}/{1}".format(os.path.dirname(os.path.abspath(__file__)), "/data/schema/platformsh.routes.json")
with open(platformshRoutesSchemaFile) as json_data:
    PLATFORMSH_SCHEMA_ROUTES = json.load(json_data)

platformshServicesSchemaFile = "{0}/{1}".format(os.path.dirname(os.path.abspath(__file__)), "/data/schema/platformsh.services.json")
with open(platformshServicesSchemaFile) as json_data:
    PLATFORMSH_SCHEMA_SERVICES = json.load(json_data)

# UPSUN_SCHEMA = {
#     "type": "object",
#     "properties": {
#         "applications": {
#             "type": "object",
#             "minProperties": 1,
#             "additionalProperties": {
#                 "type": "object",
#                 "properties": {
#                     "type": {
#                         "type": "string",
#                         "pattern": "^(nodejs|php|python|golang|ruby|java|dotnet|static|clojure|elixir|perl|sbcl|perlcgi|phpcgi|rust|bun)[@:][0-9]+(\\.[0-9]+)*$",
#                         "x-service-validator": validate_service_version
#                     },
#                     # Rest of the schema remains the same
#                     "stack": {
#                         "type": "array",
#                         "items": {
#                             "oneOf": [
#                                 {"type": "string"},
#                                 {
#                                     "type": "object",
#                                     "properties": {
#                                         "extensions": {"type": "array", "items": {"type": "string"}},
#                                         "version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+(\\.[0-9]+)?$"}
#                                     }
#                                 }
#                             ]
#                         }
#                     },
#                     # ... rest of the properties ...
#                 },
#                 "oneOf": [
#                     {"required": ["type"]},
#                     {"required": ["stack"]}
#                 ],
#                 "additionalProperties": False
#             }
#         },
#         # Rest of the schema remains the same ...
#         "services": {
#             "type": "object",
#             "additionalProperties": {
#                 "type": "object",
#                 "properties": {
#                     "type": {
#                         "type": "string",
#                         "pattern": "^(mariadb|mysql|oracle-mysql|postgresql|redis|memcached|rabbitmq|solr|elasticsearch|mongodb|mongodb-enterprise|influxdb|kafka|varnish|opensearch):[0-9]+(\\.[0-9]+)*$"
#                     },
#                     # ... rest of the services properties ...
#                 },
#                 "required": ["type"],
#                 "additionalProperties": False
#             }
#         },
#         # ... rest of the schema remains the same ...
#     },
#     "required": ["applications"],
#     "additionalProperties": False
# }