import re
import difflib

from upsunvalidator.schemas.services import SERVICE_VERSIONS

#######################################################################################################################

def validate_service_schema(service_type, service_name, service_or_runtime):
    """
    Validate that the service or runtime adheres to the `SERVICE_OR_RUNTIME_TYPE:VERSION` format requirement.
    """
    # Regex to parse service:version
    match = re.match(r'^([\w-]+):(.+)$', service_type)
    if not match:
        error_message = f"""

  Invalid service type format. Must use ':' separator in '{service_type}'

✔ Recommendation: 

  Update your configuration to use the correct formatting for specifying {service_or_runtime} types.
"""

        if service_or_runtime == "service":
            error_message += f"""
  Example: 

    ```
    services:
      SERVICE_NAME:
        type: 'SERVICE_TYPE:SUPPORTED_VERSION'
    ```
    """
        else:
            error_message += f"""
  Example: 

    ```
    applications:
      APPLICATION_NAME:
        type: 'RUNTIME_TYPE:SUPPORTED_VERSION'
    ```
    """

        return False, error_message

    return True, None

#######################################################################################################################

def validate_service_type(service_type, service_name, service_or_runtime):
    # Regex to parse service:version
    match = re.match(r'^([\w-]+):(.+)$', service_type)
    service, version = match.groups()

    # Check if service is supported generally.
    if service not in SERVICE_VERSIONS:
        # Handle invalid service types passed from validating the `services` block:
        if service_or_runtime == "service":
            valid_services = [key for key in SERVICE_VERSIONS if not SERVICE_VERSIONS[key]["runtime"]]
            # A few options for settings a default recommended service on failure.
            # recommended_service = SERVICE_VERSIONS[valid_services[0]]["type"]
            # recommended_runtime = SERVICE_VERSIONS[random.choice(valid_services)]["type"]
            recommended_service = "opensearch"
            recommended_intro = "Example:"
            valid_versions = SERVICE_VERSIONS[recommended_service]["versions"]
            service_type_clean, service_version_clean = service_type.split(":")
            # Try to guess what the user was trying to configure, in case of typos.
            if difflib.get_close_matches(service_type_clean, valid_services):
                # If there's a match, inlcude the potential typo in the recommended snippet.
                recommended_service = difflib.get_close_matches(service_type_clean, valid_services)[0]
                recommended_intro = f"Perhaps you meant to configure the runtime '{recommended_service}'?\n\n  Example:"
                # Initially, update the version for the typo'd service to the latest.
                valid_versions = SERVICE_VERSIONS[recommended_service]["versions"]
                # If the typo'd version provided by user is valid, use that instead of the latest.
                if service_version_clean in SERVICE_VERSIONS[recommended_service]["versions"]:
                    valid_versions = [service_version_clean]
            error_message = f"""

  Unsupported {service_or_runtime} type '{service}'. Supported {service_or_runtime}s are: \n\n    --> {', '.join(valid_services)}
  
✔ Recommendation: 

  Update your configuration for the {service_or_runtime} '{service_name}' to use one of the supported {service_or_runtime}s listed above.

  {recommended_intro}

    ```
    services:
      {service_name}:
        type: '{recommended_service}:{valid_versions[0]}'
    ```
"""
        # Handle invalid service types passed from validating the `applications` block:
        else:
            valid_runtimes = [key for key in SERVICE_VERSIONS if SERVICE_VERSIONS[key]["runtime"]]
            # recommended_runtime = SERVICE_VERSIONS[valid_runtimes[0]]["type"]
            # recommended_runtime = SERVICE_VERSIONS[random.choice(valid_runtimes)]["type"]
            recommended_runtime = "elixir"
            recommended_intro = f"Update your configuration for the {service_or_runtime} '{service_name}' to use one of the supported {service_or_runtime}s listed above.\n\n  Example:"
            valid_versions = SERVICE_VERSIONS[recommended_runtime]["versions"]
            service_type_clean, service_version_clean = service_type.split(":")
            if difflib.get_close_matches(service_type_clean, valid_runtimes):
                recommended_runtime = difflib.get_close_matches(service_type_clean, valid_runtimes)[0]
                recommended_intro = f"Did you mean to configure the runtime '{recommended_runtime}' instead of '{service}'?\n\n  Example:"
                valid_versions = SERVICE_VERSIONS[recommended_runtime]["versions"]
                if service_version_clean in SERVICE_VERSIONS[recommended_runtime]["versions"]:
                    valid_versions = [service_version_clean]

            error_message = f"""

  Unsupported {service_or_runtime} type '{service}'. Supported {service_or_runtime}s are: \n\n    --> {', '.join(valid_runtimes)}
  
✔ Recommendation: 

  {recommended_intro} 

    ```
    applications:
      {service_name}:
        type: '{recommended_runtime}:{valid_versions[0]}'
    ```
"""
        return False, error_message

    # Catch service types that are valid under 'services', but not under 'applications'.
    valid_runtimes = [key for key in SERVICE_VERSIONS if SERVICE_VERSIONS[key]["runtime"]]
    if ( service_or_runtime == "runtime" ) and not SERVICE_VERSIONS[service_type.split(":")[0]]["runtime"]:
        # recommended_runtime = SERVICE_VERSIONS[valid_runtimes[0]]["type"]
        recommended_runtime = "elixir"
        valid_versions = SERVICE_VERSIONS[recommended_runtime]["versions"]
        error_message = f"""

  Unsupported runtime type '{service}'. '{service}' is valid only when configuring services in the 'services' configuration block. Supported runtimes are: \n\n    · {'\n    · '.join(valid_runtimes)}

✔ Recommendation: 

  Update your configuration to use a valid runtime from the list above.

  Example: 

    ```
    applications:
      {service_name}:
        type: '{recommended_runtime}:{valid_versions[0]}'
    ```
"""
        return False, error_message

    # Catch runtime types that are valid under 'applications', but not under 'services'.
    valid_services = [key for key in SERVICE_VERSIONS if not SERVICE_VERSIONS[key]["runtime"]]
    if ( service_or_runtime == "service" ) and SERVICE_VERSIONS[service_type.split(":")[0]]["runtime"]:
        # recommended_service = SERVICE_VERSIONS[valid_services[0]]["type"]
        recommended_service = "opensearch"
        valid_versions = SERVICE_VERSIONS[recommended_service]["versions"]
        error_message = f"""

  Unsupported runtime type '{service}'. '{service}' is valid only when configuring runtimes in the 'applications' configuration block. Supported services are: \n\n    · {'\n    · '.join(valid_services)}

✔ Recommendation: 

  Update your configuration to use a valid service from the list above.

  Example: 

    ```
    services:
      {service_name}:
        type: '{recommended_service}:{valid_versions[0]}'
    ```
"""
        return False, error_message

    return True, None

#######################################################################################################################

def validate_service_version(service_type, service_name, service_or_runtime):

    # Regex to parse service:version
    match = re.match(r'^([\w-]+):(.+)$', service_type)
    
    service, version = match.groups()

    # Check version format and allowed versions
    valid_versions = SERVICE_VERSIONS[service]["versions"]
    # Support exact version match or x-based versions
    if version == 'x' or version.endswith('.x'):
        # Remove .x to check major version
        version_base = version.rstrip('.x')
        if any(v.startswith(version_base) for v in valid_versions):
            return True, None
    
    # Exact version match
    if version in valid_versions:
        return True, None

    if service_or_runtime == "service":
        error_message = f"""

  Unsupported version '{version}' for {service_or_runtime} '{service}'. Supported versions are: \n\n    · {'\n    · '.join(valid_versions)}

✔ Recommendation:

  Update your configuration for the service '{service_name}' to use one of the supported versions listed above.

  Example:

    ```
    services:
      {service_name}:
        type: '{service}:{valid_versions[0]}'
    ```
"""
    else:
        error_message = f"""

  Unsupported version '{version}' for {service_or_runtime} '{service}'. Supported versions are: \n\n    · {'\n    · '.join(valid_versions)}

✔ Recommendation:

  Update your configuration for the runtime '{service_name}' to use one of the supported versions listed above.

  Example:

    ```
    applications:
      {service_name}:
        type: '{service}:{valid_versions[0]}'
    ```
"""
    
    return False, error_message
