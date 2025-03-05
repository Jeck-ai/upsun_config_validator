import os
import json

PLATFORMSH_PROPER_NAME="Platform.sh"

# PLATFORMSH
platformshAppSchemaFile = "{0}/{1}".format(os.path.dirname(os.path.abspath(__file__)), "/data/providers/platformsh.application.json")
with open(platformshAppSchemaFile) as json_data:
    PLATFORMSH_SCHEMA_APPS = json.load(json_data)

# @todo: OVERRIDE: Some spec overrides, which will need investigation
# web.locations - default value is -1 (int) for expected type string
PLATFORMSH_SCHEMA_APPS["properties"]["web"]["properties"]["locations"]["additionalProperties"]["properties"]["expires"]["type"] = ["string", "integer"]

platformshRoutesSchemaFile = "{0}/{1}".format(os.path.dirname(os.path.abspath(__file__)), "/data/providers/platformsh.routes.json")
with open(platformshRoutesSchemaFile) as json_data:
    PLATFORMSH_SCHEMA_ROUTES = json.load(json_data)

platformshServicesSchemaFile = "{0}/{1}".format(os.path.dirname(os.path.abspath(__file__)), "/data/providers/platformsh.services.json")
with open(platformshServicesSchemaFile) as json_data:
    PLATFORMSH_SCHEMA_SERVICES = json.load(json_data)
