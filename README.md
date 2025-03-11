
<p align="right">
<a href="https://jeck.ai">
<img src="https://avatars.githubusercontent.com/u/198296402?s=200&v=4" width="150px">
</a>
</p>

<!-- <p align="center">
<a href="https://www.drupal.org/">
<img src="header.svg">
</a>
</p> -->

<h1 align="center">upsunvalidator</h1>

<p align="center">
<strong>Contribute, request a feature, or check out our resources</strong>
<br />
<br />
<a href="https://jeck.ai"><strong>Give us a try</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="https://jeck.ai/blog"><strong>Blog</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="https://github.com/platformsh-templates/drupal11/issues/new?assignees=&labels=bug&template=bug_report.yml"><strong>Report a bug</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="https://github.com/platformsh-templates/drupal11/issues/new?assignees=&labels=feature+request&template=improvements.yml"><strong>Request a feature</strong></a>
<br /><br />
</p>

<p align="center">
<a href="https://github.com/Jeck-ai/upsun_config_validator/issues">
<img src="https://img.shields.io/github/issues/Jeck-ai/upsun_config_validator.svg?style=for-the-badge&labelColor=f4f2f3&color=3c724e&label=Issues" alt="Open issues" />
</a>&nbsp&nbsp
<a href="https://github.com/Jeck-ai/upsun_config_validator/pulls">
<img src="https://img.shields.io/github/issues-pr/Jeck-ai/upsun_config_validator.svg?style=for-the-badge&labelColor=f4f2f3&color=3c724e&label=Pull%20requests" alt="Open PRs" />
</a>&nbsp&nbsp
<a href="https://github.com/Jeck-ai/upsun_config_validator/blob/master/LICENSE">
<img src="https://img.shields.io/static/v1?label=License&message=MIT&style=for-the-badge&labelColor=f4f2f3&color=3c724e" alt="License" />
</a>
</p>

<hr>

<p align="center">
<br />
<a href="#about"><strong>About</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="#getting-started"><strong>Getting started</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="#migrate"><strong>Migrate</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="#learn"><strong>Learn</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="#contribute"><strong>Contribute</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<br />
</p>
<hr>

A Python-based validator for Upsun (formerly Platform.sh) configuration files. 
This tool helps catch configuration errors before deployment by validating configuration YAML files against the official Upsun & Platform.sh schemas.

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
python3 -m venv venv
source venv/bin/activate
pip install .
```

## Usage

To validate a project:

```bash
# Run a validation
upsunvalidator validate --src $PATH_TO_CONFIG_FILES --provider upsun
upsunvalidator validate --src $PATH_TO_CONFIG_FILES --provider platformsh
```

## Testing

The project includes a comprehensive test suite:

```bash
python3 -m venv venv
source venv/bin/activate
pip install .
pytest
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
