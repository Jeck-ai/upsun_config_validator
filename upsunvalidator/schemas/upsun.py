import os
import json

UPSUN_PROPER_NAME="Upsun"

# UPSUN SCHEMA
upsunSchemaFile = "{0}/{1}".format(os.path.dirname(os.path.abspath(__file__)), "/data/providers/upsun.json")
with open(upsunSchemaFile) as json_data:
    UPSUN_SCHEMA = json.load(json_data)

    # @todo: Some spec overrides, which will need investigation
    UPSUN_SCHEMA["properties"]["applications"]["additionalProperties"]["properties"]["web"]["properties"]["locations"]["additionalProperties"]["properties"]["expires"]["type"] = ["string", "integer"]
