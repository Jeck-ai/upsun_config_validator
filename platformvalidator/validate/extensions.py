import itertools
from platformvalidator.schemas.extensions import PHP_EXTENSIONS

def validate_php_extensions(runtime, php_version):
    # Get the keys straight.
    valid_extensions_key = "extensions"
    schema_valid_extensions_key = PHP_EXTENSIONS["valid"][valid_extensions_key]
    valid_disable_extensions_key = "disabled_extensions"
    schema_valid_disable_extensions_key = PHP_EXTENSIONS["valid"][valid_disable_extensions_key]
    invalid_disable_extensions_key = "built-in"
    schema_invalid_disable_extensions_key = PHP_EXTENSIONS["valid"][invalid_disable_extensions_key]
    with_webp_extensions_key = "with-webp"
    schema_with_webp_extensions_key = PHP_EXTENSIONS["valid"][with_webp_extensions_key]

    # Validate valid extensions that can be enabled for the PHP version.
    if valid_extensions_key in runtime:
        all_supported_extensions = list(itertools.chain(PHP_EXTENSIONS["extensions_by_version"][php_version][schema_valid_extensions_key],
            PHP_EXTENSIONS["extensions_by_version"][php_version][schema_invalid_disable_extensions_key],
            PHP_EXTENSIONS["extensions_by_version"][php_version][schema_valid_disable_extensions_key],
            PHP_EXTENSIONS["extensions_by_version"][php_version][schema_with_webp_extensions_key]) )
        for extension in runtime[valid_extensions_key]:
            if extension not in all_supported_extensions:
                return False, f"Extension {extension} is not supported in PHP {php_version}. Supported extensions are: {', '.join(all_supported_extensions)}"
         
    # Validate disabled extensions that can be disabled (are enabled by default) for the PHP version.
    if valid_disable_extensions_key in runtime:
        for extension in runtime[valid_disable_extensions_key]:
            if extension not in PHP_EXTENSIONS["extensions_by_version"][php_version][schema_valid_disable_extensions_key]:
                return False, f"Extension {extension} cannot be disabled in PHP {php_version}. Valid extensions to disable are: {', '.join(PHP_EXTENSIONS['extensions_by_version'][php_version][schema_valid_disable_extensions_key])}"

    # Ensure that extensions aren't under 'disabled_extensions' but cannot actually be turned off (built-in)
    if valid_disable_extensions_key in runtime:
        for extension in runtime[valid_disable_extensions_key]:
            if extension in PHP_EXTENSIONS["extensions_by_version"][php_version][schema_invalid_disable_extensions_key]:
                return False, f"Extension {extension} is built-in for PHP {php_version}, and cannot be disabled"

    return True, None
