import yaml

import sys
sys.tracebacklimit=0

from jsonschema import validate

from upsunvalidator.schemas.platformsh import PLATFORMSH_SCHEMA_APPS, PLATFORMSH_SCHEMA_ROUTES, PLATFORMSH_SCHEMA_SERVICES

from upsunvalidator.utils.utils import load_yaml_file, flatten_validation_error
from upsunvalidator.validate.services import validate_service_version, validate_service_schema, validate_service_type, validate_service_version
from upsunvalidator.validate.extensions import validate_php_extensions

from upsunvalidator.validate.errors import InvalidServiceVersionError, ValidationError, InvalidPHPExtensionError, InvalidServiceTypeError, InvalidServiceSchemaError, InvalidServiceVersionError


def validate_platformsh_config(yaml_files):
    if "platformsh" in yaml_files:
        configAppFiles = []
        configRoutes = None
        configServices = None

        for file in yaml_files["platformsh"]:
            try:
                data = yaml.safe_load(load_yaml_file(file))
            except yaml.YAMLError as e:
                return [f"YAML parsing error: {e}"]
                        
            if data is not None:
                if ("name" in data) or ("applications" in data) or ((isinstance(data, list)) and ("name" in data[0])):
                    configAppFiles.append(data)
                elif ("https://{default}/" in data) or ("https://{default}" in data):
                    configRoutes = data
                else:
                    configServices = data

    else:
        return ["✔ No errors found. YAML is valid.\n"]

    # Apps.
    if configAppFiles is None:
        return ["YAML parsing error: Empty configuration"]
    if configAppFiles:
        for configApp in configAppFiles:
            # Custom service version validation
            if 'applications' in configApp:
                for app_name, app_config in configApp['applications'].items():
                    if 'type' in app_config:
                        # Validate the 'type' schema.
                        is_valid, error_message = validate_service_schema(app_config['type'], app_name, "runtime")
                        if not is_valid:
                            raise InvalidServiceSchemaError(f"\n\n✘ Error found in application '{app_name}'{error_message}")
                        # Validate the type.
                        is_valid, error_message = validate_service_type(app_config['type'], app_name, "runtime")
                        if not is_valid:
                            raise InvalidServiceTypeError(f"\n\n✘ Error found in application '{app_name}':{error_message}")
                        # Validate the runtime versions.
                        is_valid, error_message = validate_service_version(app_config['type'], app_name, "runtime")
                        if not is_valid:
                            raise InvalidServiceVersionError(f"\n\n✘ Error found in application '{app_name}':{error_message}")
                        # Validate PHP extensions if defined.
                        if "php" in app_config["type"]:
                            php_version = app_config["type"].split(":")[1]
                            if "runtime" in app_config:
                                if ( "extensions" in app_config["runtime"] ) or ( "disabled_extensions" in app_config["runtime"] ):
                                    is_valid, error_message = validate_php_extensions(app_config["runtime"], php_version, app_name)
                                    if not is_valid:
                                        raise InvalidPHPExtensionError(f"\n\n✘ Error found in application '{app_name}':{error_message}")
                    # Validate against the application schema.
                    validate(instance=app_config, schema=PLATFORMSH_SCHEMA_APPS)

            elif 'type' in configApp:
                app_config = configApp
                app_name = app_config["name"]
                # Validate the 'type' schema.
                is_valid, error_message = validate_service_schema(app_config['type'], app_name, "runtime")
                if not is_valid:
                    raise InvalidServiceSchemaError(f"\n\n✘ Error found in application '{app_name}'{error_message}")
                # Validate the type.
                is_valid, error_message = validate_service_type(app_config['type'], app_name, "runtime")
                if not is_valid:
                    raise InvalidServiceTypeError(f"\n\n✘ Error found in application '{app_name}':{error_message}")
                # Validate the runtime versions.
                is_valid, error_message = validate_service_version(app_config['type'], app_name, "runtime")
                if not is_valid:
                    raise InvalidServiceVersionError(f"\n\n✘ Error found in application '{app_name}':{error_message}")
                # Validate PHP extensions if defined.
                if "php" in app_config["type"]:
                    php_version = app_config["type"].split(":")[1]
                    if "runtime" in app_config:
                        if ( "extensions" in app_config["runtime"] ) or ( "disabled_extensions" in app_config["runtime"] ):
                            is_valid, error_message = validate_php_extensions(app_config["runtime"], php_version, app_name)
                            if not is_valid:
                                raise InvalidPHPExtensionError(f"\n\n✘ Error found in application '{app_name}':{error_message}")
                # Validate against the application schema.
                validate(instance=app_config, schema=PLATFORMSH_SCHEMA_APPS)
                
            elif isinstance(configApp, list):
                for app_config in configApp:
                    if 'type' in app_config:
                        app_name = app_config["name"]
                        # Validate the 'type' schema.
                        is_valid, error_message = validate_service_schema(app_config['type'], app_name, "runtime")
                        if not is_valid:
                            raise InvalidServiceSchemaError(f"\n\n✘ Error found in application '{app_name}'{error_message}")
                        # Validate the type.
                        is_valid, error_message = validate_service_type(app_config['type'], app_name, "runtime")
                        if not is_valid:
                            raise InvalidServiceTypeError(f"\n\n✘ Error found in application '{app_name}':{error_message}")
                        # Validate the runtime versions.
                        is_valid, error_message = validate_service_version(app_config['type'], app_name, "runtime")
                        if not is_valid:
                            raise InvalidServiceVersionError(f"\n\n✘ Error found in application '{app_name}':{error_message}")
                        # Validate PHP extensions if defined.
                        if "php" in app_config["type"]:
                            php_version = app_config["type"].split(":")[1]
                            if "runtime" in app_config:
                                if ( "extensions" in app_config["runtime"] ) or ( "disabled_extensions" in app_config["runtime"] ):
                                    is_valid, error_message = validate_php_extensions(app_config["runtime"], php_version, app_name)
                                    if not is_valid:
                                        raise InvalidPHPExtensionError(f"\n\n✘ Error found in application '{app_name}':{error_message}")
                        # Validate against the application schema.
                        validate(instance=app_config, schema=PLATFORMSH_SCHEMA_APPS)

    # Routes.
    if configRoutes is not None:
        validate(instance=configRoutes, schema=PLATFORMSH_SCHEMA_ROUTES)

    # Services.
    if configServices is not None:
        for service_name, service_config in configServices.items():
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

        validate(instance=configServices, schema=PLATFORMSH_SCHEMA_SERVICES)

    return ["✔ No errors found. YAML is valid.\n"]
