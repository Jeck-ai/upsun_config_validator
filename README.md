# Upsun Config Validator

A Python-based validator for Upsun (formerly Platform.sh) configuration files. This tool helps catch configuration errors before deployment by validating `.upsun/config.yaml` files against the official Upsun schema.

## Features

- Validates application runtimes and their versions
- Validates service configurations
- Validates route patterns and configurations
- Provides clear error messages for invalid configurations
- Includes test suite with passing and failing examples

## Installation

```bash
# Clone the repository
git clone git@github.com:Jeck-ai/upsun_config_validator.git

# Install the validator
cd upsun_config_validator
pip install --editable .
```

## Usage

To validate a project:

```bash
# Run a validation
upsunvalidator validate --src $PATH_TO_CONFIG_FILES --provider upsun
upsunvalidator validate --src $PATH_TO_CONFIG_FILES --provider platformsh
```
<!-- 
```python
from validator import validate_upsun_config

with open('path/to/.upsun/config.yaml', 'r') as f:
    yaml_content = f.read()
    
errors = validate_upsun_config(yaml_content)
if errors == ["No errors found. YAML is valid."]:
    print("Configuration is valid!")
else:
    print("Validation errors found:")
    for error in errors:
        print(f"- {error}")
``` -->

## Testing

The project includes a comprehensive test suite:

```bash
pipenv install
pipenv run pytest
```

<!-- Test files are organized in two directories:
- `tests/passing_configs/`: Examples of valid configurations
- `tests/failing_configs/`: Examples of invalid configurations

## Documentation

- `docs/routes.md`: Documentation of valid route patterns
- More documentation coming soon -->

## License

MIT

## Contributing

We're very interested in adding to the passing configs. If you have working configuration files for Platform.sh and/or Upsun, please share!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Add you configuration to the `tests/valid` using the pattern `tests/valid/YOUR_EXAMPLE_OR_FRAMEWORK_NAME/files/...`
4. Commit your changes (`git commit -am 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request
