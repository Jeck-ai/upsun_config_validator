
<p align="center">
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
<a href="https://jeck.ai"><strong>Check out Jeck.ai</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="https://jeck.ai/blog"><strong>Blog</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="https://github.com/Jeck-ai/upsun_config_validator/issues/new?assignees=&labels=bug&template=bug-report.yml"><strong>Report a bug</strong></a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
<a href="https://github.com/Jeck-ai/upsun_config_validator/issues/new?assignees=&labels=feature+request&template=improvements.yml"><strong>Request a feature</strong></a>
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

A Python-based validator for Upsun (formerly Platform.sh) configuration files. 
This tool helps catch configuration errors before deployment by validating configuration YAML files against the official Upsun & Platform.sh schemas.

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

- Validates application runtimes, services, and their versions
- Validates application and service configurations
- Validates route patterns and configurations
- Provides clear error messages for invalid configurations
- Provides recommendations when possible
- Includes test suite with passing and failing examples

## Installation

**Requirements:**

> [!IMPORTANT]  
> `upsunvalidator` requires at least Python 3.12.

```bash
pip install upsunvalidator
# or
python -m pip install --user upsunvalidator
```

You can then check the installed version with:

```bash
upsunvalidator version
```

### Upgrade

```bash
python -m pip install --user upsunvalidator --upgrade
```

## Usage

### Validating project code for various PaaS providers

1. Provider: Upsun

    ```bash
    # If executing from within the repository, pwd will be used.
    upsunvalidator validate --provider upsun
    # or
    upv validate --provider upsun

    # If outside the project dir, use the --src flag
    upsunvalidator validate --src $PATH_TO_REPO --provider upsun
    # or
    upv validate --src $PATH_TO_REPO --provider upsun
    ```

2. Provider: Platform.sh

    ```bash
    # If executing from within the repository, pwd will be used.
    upsunvalidator validate --provider platformsh
    # or
    upv validate --provider platformsh

    # If outside the project dir, use the --src flag
    upsunvalidator validate --src $PATH_TO_REPO --provider platformsh
    # or
    upv validate --src $PATH_TO_REPO --provider platformsh
    ```

3. All providers

    ```bash
    # If executing from within the repository, pwd will be used.
    upsunvalidator validate
    # or
    upv validate

    # If outside the project dir, use the --src flag
    upsunvalidator validate --src $PATH_TO_REPO
    # or
    upv validate --src $PATH_TO_REPO
    ```

## Testing

The project includes a comprehensive test suite:

```bash
python3 -m venv venv
source venv/bin/activate
pip install .
pytest
```

## License

[MIT License](./LICENSE)

## Contribute

We're very interested in adding to the passing configs. If you have working configuration files for Platform.sh and/or Upsun, please share!

1. Create an issue
2. Fork the repository
3. Create your feature branch (`git checkout -b feature/amazing-feature`)
4. Add you configuration to the `tests/valid` using the pattern `tests/valid/YOUR_EXAMPLE_OR_FRAMEWORK_NAME/files/...`
5. Commit your changes (`git commit -am 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for more details.