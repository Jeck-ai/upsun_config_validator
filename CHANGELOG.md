# Changelog

## [0.0.1] - 2025-03-05

### Added

For the first release of `platformvalidator`, this library contains the following capabilities:

1. Leverages the pre-existing schema validation for Platform.sh and Upsun provided by the `app:config-validate` command.
1. Validates valid service versions for both applications and services, as documented in the Platform.sh and Upsun public documentation.
1. Validates valid PHP extensions for PHP application types, as documented in the Platform.sh and Upsun public documentation.
1. Leverages a collection of working Platform.sh and Upsun templates as a part of internal testing.

At this point, this library does not yet handle:

1. Multi-app configurations.
1. Nix-based composable images.

@todo

- [ ] Finish packaging with Typer so single file/executable can be run via MCP
- [ ] contributing examples instructions
- [ ] issue and pull request templates
- [ ] rename repo to match publish path
- [ ] set pypi api token for publish action
- [ ] setup recurring actions to pull upsun/p.sh schemas, extensions.yaml, and registry.json
- [ ] Update readme
