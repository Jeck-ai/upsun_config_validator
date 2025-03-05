import os
import yaml

# PHP extensions file.
phpExtensionsFile = "{0}/{1}".format(os.path.dirname(os.path.abspath(__file__)), "/data/extensions/php_extensions.yaml")
with open(phpExtensionsFile) as stream:
    try:
        data = yaml.safe_load(stream)
        PHP_EXTENSIONS = {
            "valid": {
                "extensions": "available",
                "disabled_extensions": "default",
                "built-in": "built-in",
                "with-webp": "with-webp"
            },
            "extensions_by_version": data["grid"]
        }
    except yaml.YAMLError as exc:
        print(exc)
