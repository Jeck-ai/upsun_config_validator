import os 

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Valid tests.
PASSING_DIR = os.path.join(TESTS_DIR, 'valid')

# Failing tests.
INVALID_RUNTIME_VERSION_DIR = os.path.join(TESTS_DIR, 'invalid_runtime_versions')
INVALID_SERVICE_VERSION_DIR = os.path.join(TESTS_DIR, 'invalid_service_versions')
INVALID_ENABLE_PHP_EXTENSIONS_DIR = os.path.join(TESTS_DIR, 'invalid_enable_php_extensions')
INVALID_TOP_LEVEL_KEYS_DIR = os.path.join(TESTS_DIR, 'invalid_toplevel_keys')

