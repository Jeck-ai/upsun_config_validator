
<p align="center">
<a href="https://jeck.ai">
<img src="https://avatars.githubusercontent.com/u/198296402?s=200&v=4" width="150px">
</a>
</p>

<h1 align="center">upsunvalidator</h1>

<p align="center">
<strong>Contribute, request a feature, or check out our resources</strong>
<br />
<br />
<a href="https://jeck.ai"><strong>Check out Jeck.ai</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="https://jeck.ai/blog"><strong>Blog</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="https://github.com/Jeck-ai/mcp-cli-framework-go/issues/new?assignees=&labels=bug&template=bug-report.yml"><strong>Report a bug</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="https://github.com/Jeck-ai/mcp-cli-framework-go/issues/new?assignees=&labels=feature+request&template=improvements.yml"><strong>Request a feature</strong></a>
<br /><br />
</p>

<p align="center">
<a href="https://github.com/Jeck-ai/upsunvalidator/issues">
<img src="https://img.shields.io/github/issues/Jeck-ai/upsunvalidator.svg?style=for-the-badge&labelColor=f4f2f3&color=3c724e&label=Issues" alt="Open issues" />
</a>&nbsp&nbsp
<a href="https://github.com/Jeck-ai/upsunvalidator/pulls">
<img src="https://img.shields.io/github/issues-pr/Jeck-ai/upsunvalidator.svg?style=for-the-badge&labelColor=f4f2f3&color=3c724e&label=Pull%20requests" alt="Open PRs" />
</a>&nbsp&nbsp
<a href="https://github.com/Jeck-ai/upsunvalidator/blob/master/LICENSE">
<img src="https://img.shields.io/static/v1?label=License&message=MIT&style=for-the-badge&labelColor=f4f2f3&color=3c724e" alt="License" />
</a>
</p>

<hr>

A Python-based validator library for Upsun configuration files. 
This library enforces strict schema validation to catch configuration errors before deployment by validating YAML files against the official Upsun JSON schema.

<p align="center">
<br />
<a href="#features"><strong>Features</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="#installation"><strong>Installation</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="#usage"><strong>Usage</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="#testing"><strong>Testing</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="#license"><strong>License</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="#contribute"><strong>Contribute</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<br />
</p>

## Features

- Validates configuration structure using strict JSON schema enforcement
- Prevents invalid top-level properties (blocks Docker Compose style configs)
- Enforces correct data types for all properties (strings vs integers)
- Validates application runtimes, services, and their versions
- Validates application and service configurations
- Validates route patterns and configurations
- Provides detailed error messages with specific validation failures
- Provides recommendations when possible
- Includes comprehensive test suite with passing and failing examples
- Provides access to example configuration templates for various frameworks

## Installation

**Requirements:**

> [!IMPORTANT]  
> `upsunvalidator` requires Python 3.12 or newer (tested with Python 3.13).

```bash
pip install upsunvalidator
```

You can then check the installed version with:

### Upgrade

```bash
pip install --upgrade upsunvalidator
```

## Usage

### Using in your code

```python
from upsunvalidator import validate, validate_string

# Validate project in current directory
success, message = validate()
print(message)

# Validate project in specific directory
success, message = validate("/path/to/project")
print(message)

# Validate a configuration string directly
config_content = """
applications:
  app:
    type: php:8.2
    relationships:
      database: 'db:mysql'
      
services:
  db:
    type: mariadb:10.11
  
routes:
  "https://{default}/":
    type: upstream
    upstream: "app:http"
"""
success, message = validate_string(config_content)
print(message)

# Example of invalid config with schema violation
invalid_config = """
applications:
  app:
    type: php:8.2
    
# Invalid properties at root level will be caught
version: '3.8'
networks:
  frontend:
    driver: bridge
"""
success, message = validate_string(invalid_config)
print(message)  # Will show error about additional properties not allowed

# Example of data type validation
invalid_type_config = """
applications:
  app:
    type: php:8.2
    resources:
      base_memory: '128'  # String instead of required integer
"""
success, message = validate_string(invalid_type_config)
print(message)  # Will show error about type mismatch
```

### Using the template library

```python
from upsunvalidator import get_available_template_names, get_template_config, get_template_config_with_info

# Get list of available template names
template_names = get_available_template_names()
print(template_names)  # ['akeneo', 'directus', 'django4', 'drupal11', 'express', ...]

# Get a specific template's config.yaml content
wordpress_config = get_template_config('wordpress-vanilla')
print(wordpress_config)  # YAML content as string

# Get templates with descriptions for easier selection
templates_info = get_template_config_with_info()
for name, (description, _) in templates_info.items():
    print(f"{name}: {description}")

# Get and use a specific template
laravel_config = get_template_config('laravel')
if laravel_config:
    # Validate the template
    from upsunvalidator import validate_string
    success, message = validate_string(laravel_config)
    print(message)
```

## Testing

The project includes a comprehensive test suite:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install .
pytest
```

## License

[MIT License](./LICENSE)

## Contribute

We're very interested in adding to the passing configs. If you have working configuration files for Upsun, please share!

1. Create an issue
2. Fork the repository
3. Create your feature branch (`git checkout -b feature/amazing-feature`)
4. Add you configuration to the `upsunvalidator/tests/valid` using the pattern `upsunvalidator/tests/valid/YOUR_EXAMPLE_OR_FRAMEWORK_NAME/.upsun/config.yaml`
5. Commit your changes (`git commit -am 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for more details.