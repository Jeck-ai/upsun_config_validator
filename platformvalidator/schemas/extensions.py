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
        for key in PHP_EXTENSIONS["valid"]:
            for version in PHP_EXTENSIONS["extensions_by_version"]:
                if key not in PHP_EXTENSIONS["extensions_by_version"][version]:
                    PHP_EXTENSIONS["extensions_by_version"][version][key] = []
    except yaml.YAMLError as exc:
        print(exc)
