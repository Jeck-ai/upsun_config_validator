# @pytest.mark.parametrize("current_template", get_all_projects_in_directory(INVALID_ENABLE_PHP_EXTENSIONS_DIR, "files"))
# def test_invalid_enable_php_extensions(current_template):
#     yaml_files = get_yaml_files(current_template)

#     valid_extensions_key = "extensions"
#     schema_valid_extensions_key = PHP_EXTENSIONS["valid"][valid_extensions_key]
#     valid_disable_extensions_key = "disabled_extensions"
#     schema_valid_disable_extensions_key = PHP_EXTENSIONS["valid"][valid_disable_extensions_key]
#     invalid_disable_extensions_key = "built-in"
#     schema_invalid_disable_extensions_key = PHP_EXTENSIONS["valid"][invalid_disable_extensions_key]
#     with_webp_extensions_key = "with-webp"
#     schema_with_webp_extensions_key = PHP_EXTENSIONS["valid"][with_webp_extensions_key]

#     if "upsun" in yaml_files:
#         data = yaml.safe_load(load_yaml_file(yaml_files["upsun"][0]))
#         app_name = list(data["applications"].keys())[0]
#         php_version = data["applications"][app_name]["type"].split(":")[1]

#         # if schema_with_webp_extensions_key not in PHP_EXTENSIONS["extensions_by_version"][php_version]:
#         #     PHP_EXTENSIONS["extensions_by_version"][php_version][schema_with_webp_extensions_key] = []

#         invalid_extension = data["applications"][app_name]["runtime"]["extensions"][0]

#         all_supported_extensions = list(itertools.chain(PHP_EXTENSIONS["extensions_by_version"][php_version][schema_valid_extensions_key],
#             PHP_EXTENSIONS["extensions_by_version"][php_version][schema_invalid_disable_extensions_key],
#             PHP_EXTENSIONS["extensions_by_version"][php_version][schema_valid_disable_extensions_key],
#             PHP_EXTENSIONS["extensions_by_version"][php_version][schema_with_webp_extensions_key]) )
#         msg = f"\nUpsun schema validation error for runtime '{app_name}'\n✘ Extension {invalid_extension} is not supported in PHP {php_version}. Supported extensions are: {', '.join(all_supported_extensions)}\n"

#         with pytest.raises(InvalidPHPExtensionError, match=msg):
#             validate_upsun_config(yaml_files)

