import re
import os
import json


# Handle service versions.
# @todo: GH Action: periodically update supported versions
registryLocation = "{0}/{1}".format(os.path.dirname(os.path.abspath(__file__)), "/data/services/registry.json")
SERVICE_VERSIONS = {}
with open(registryLocation) as json_data:
    data = json.load(json_data)
    for key in data:
        SERVICE_VERSIONS[key] = {
            "type": key,
            "runtime": data[key]["runtime"],
            "versions": data[key]["versions"]["supported"],
        }
        if "disk" in data[key]:
            SERVICE_VERSIONS[key]["disk"] = data[key]["disk"]
        if "endpoint" in data[key]:
            SERVICE_VERSIONS[key]["endpoint"] = data[key]["endpoint"]
        if "min_disk_size" in data[key]:
            SERVICE_VERSIONS[key]["min_disk_size"] = data[key]["min_disk_size"]

        # Duplicate for the `redis-persistent` option
        if key == "redis":
            SERVICE_VERSIONS["redis-persistent"] = SERVICE_VERSIONS[key]
