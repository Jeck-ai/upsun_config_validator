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
git clone git@github.com:robertDouglass/upsun_config_validator.git

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

To validate a config file:

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
```

## Testing

The project includes a comprehensive test suite:

```bash
pytest
```

Test files are organized in two directories:
- `tests/passing_configs/`: Examples of valid configurations
- `tests/failing_configs/`: Examples of invalid configurations

## Documentation

- `docs/routes.md`: Documentation of valid route patterns
- More documentation coming soon

## License

MIT

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -am 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request