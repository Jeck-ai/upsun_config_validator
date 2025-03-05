import re

from platformvalidator.schemas.services import SERVICE_VERSIONS

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
    if service not in SERVICE_VERSIONS:
        return False, f"Unsupported service type '{service}'. Supported services are: {', '.join(SERVICE_VERSIONS.keys())}"
    
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
    
    return False, f"Unsupported version '{version}' for service '{service}'. Allowed versions are: {', '.join(valid_versions)}"
