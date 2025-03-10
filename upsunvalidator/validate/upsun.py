import yaml

import sys
sys.tracebacklimit=0

from jsonschema import validate

from upsunvalidator.schemas.upsun import UPSUN_SCHEMA

from upsunvalidator.utils.utils import load_yaml_file, flatten_validation_error
from upsunvalidator.validate.services import validate_service_version, validate_service_schema, validate_service_type, validate_service_version
from upsunvalidator.validate.extensions import validate_php_extensions

from upsunvalidator.validate.errors import InvalidServiceVersionError, ValidationError, InvalidPHPExtensionError, InvalidServiceTypeError, InvalidServiceSchemaError, InvalidServiceVersionError


def validate_upsun_config(yaml_files):

    if "upsun" in yaml_files:

        # Combine all files in this directory (Relevant for Upsun only)
        combined = {
            "applications": {},
            "services": {},
            "routes": {}
        }

        for file in yaml_files["upsun"]:
            try:
                data = yaml.safe_load(load_yaml_file(file))
            except yaml.YAMLError as e:
                return [f"YAML parsing error: {e}"]
                        
            if "applications" in data:
                combined["applications"] = combined["applications"] | data["applications"]
            if "services" in data:
                combined["services"] = combined["services"] | data["services"]
            if "routes" in data:
                combined["routes"] = combined["routes"] | data["routes"]

        if combined["routes"] == {}:
            del combined["routes"]
        if combined["services"] == {}:
            del combined["services"]

    else:
        return ["✔ No errors found. YAML is valid.\n"]

    config = combined

    if config is None:
        return ["YAML parsing error: Empty configuration"]

    if 'applications' in config:
        for app_name, app_config in config['applications'].items():
            if 'type' in app_config:
                # Validate the schema.
                is_valid, error_message = validate_service_schema(app_config['type'], app_name, "runtime")
                if not is_valid:
                    raise InvalidServiceSchemaError(f"\n\n✘ Error found in application '{app_name}'{error_message}")
                # Validate the type.
                is_valid, error_message = validate_service_type(app_config['type'], app_name, "runtime")
                if not is_valid:
                    raise InvalidServiceTypeError(f"\n\n✘ Error found in application '{app_name}':{error_message}")
                # Validate the service versions.
                is_valid, error_message = validate_service_version(app_config['type'], app_name, "runtime")
                if not is_valid:
                    raise InvalidServiceVersionError(f"\n\n✘ Error found in application '{app_name}':{error_message}")

                if "php" in app_config["type"]:
                    php_version = app_config["type"].split(":")[1]
                    if "runtime" in app_config:
                        if ( "extensions" in app_config["runtime"] ) or ( "disabled_extensions" in app_config["runtime"] ):
                            is_valid, error_message = validate_php_extensions(app_config["runtime"], php_version, app_name)
                            if not is_valid:
                                raise InvalidPHPExtensionError(f"\n\n✘ Error found in application '{app_name}':{error_message}")

    if 'services' in config:
        for service_name, service_config in config['services'].items():
            if 'type' in service_config:
                # Validate the schema.
                is_valid, error_message = validate_service_schema(service_config['type'], service_name, "service")
                if not is_valid:
                    raise InvalidServiceSchemaError(f"\n\n✘ Error found in service '{service_name}':{error_message}")
                # Validate the type.
                is_valid, error_message = validate_service_type(service_config['type'], service_name, "service")
                if not is_valid:
                    raise InvalidServiceTypeError(f"\n\n✘ Error found in service '{service_name}':{error_message}")
                # Validate the service versions.
                is_valid, error_message = validate_service_version(service_config['type'], service_name, "service")
                if not is_valid:
                    raise InvalidServiceVersionError(f"\n\n✘ Error found in service '{service_name}':{error_message}")

    validate(instance=config, schema=UPSUN_SCHEMA)

    return ["✔ No errors found. YAML is valid.\n"]
