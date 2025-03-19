import os
import json

# UPSUN SCHEMA
schema_file = "{0}/{1}".format(os.path.dirname(os.path.abspath(__file__)), "/data/providers/upsun.json")
with open(schema_file) as json_data:
    UPSUN_SCHEMA = json.load(json_data)

    # @todo: Some spec overrides, which will need investigation
    UPSUN_SCHEMA["properties"]["applications"]["additionalProperties"]["properties"]["web"]["properties"]["locations"]["additionalProperties"]["properties"]["expires"]["type"] = ["string", "integer"]
