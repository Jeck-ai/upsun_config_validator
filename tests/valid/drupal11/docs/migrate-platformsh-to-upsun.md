2025/02/19 11:38:24 ./convsun --src /Users/chadwcarlson/Code/template-builder/templates/drupal11/files
2025/02/19 11:38:24 
convsun from ADV-initial version development

2025/02/19 11:38:24 Convert Project to Upsun...
2025/02/19 11:38:24 Discover found 'routes.yaml' at: /Users/chadwcarlson/Code/template-builder/templates/drupal11/files/.platform/routes.yaml
2025/02/19 11:38:24 Discover found 'services.yaml' at: /Users/chadwcarlson/Code/template-builder/templates/drupal11/files/.platform/services.yaml
WARNING: file 'applications.yaml' not found in directory '/Users/chadwcarlson/Code/template-builder/templates/drupal11/files/.platform'
2025/02/19 11:38:24 Discover found '.platform.app.yaml' at: /Users/chadwcarlson/Code/template-builder/templates/drupal11/files/.platform.app.yaml
2025/02/19 11:38:24 Upsun does not use 'sizes' in its configuration file (config.yml) !!
	Sizing is defined in the web console.
2025/02/19 11:38:24 Remove all 'size' on services.yaml...
2025/02/19 11:38:24 Remove all 'size' on .platform.app.yaml/applications.yaml...
2025/02/19 11:38:24 Upsun uses different mount types !!
	For more information: https://docs.upsun.com/create-apps/app-reference/single-runtime-image.html#define-a-mount
2025/02/19 11:38:24 Replace all mount type on .platform.app.yaml/applications.yaml...
2025/02/19 11:38:24 - Replace 'local' by 'storage' line 31
2025/02/19 11:38:24 - Replace 'local' by 'storage' line 36
2025/02/19 11:38:24 - Replace 'local' by 'storage' line 41
2025/02/19 11:38:24 - Replace 'local' by 'storage' line 45
2025/02/19 11:38:24 - Replace 'local' by 'storage' line 50
2025/02/19 11:38:24 Upsun configuration files doesn't define 'disk' !!
	Disk is define into web console.
	For more information: https://docs.upsun.com/create-apps/app-reference/single-runtime-image.html#available-disk-space
2025/02/19 11:38:24 Remove all 'disk' on services.yaml...
2025/02/19 11:38:24 - Remove 'disk' field on line 7
2025/02/19 11:38:24 Remove all 'disk' on .platform.app.yaml/applications.yaml...
2025/02/19 11:38:24 - Remove 'disk' field on line 0
2025/02/19 11:38:24 Upsun does not use 'resources' in its configuration file (config.yml) !!
	Resources is defined in the web console.
2025/02/19 11:38:24 Remove all 'resources' on services.yaml...
2025/02/19 11:38:24 Remove all 'resources' on .platform.app.yaml/applications.yaml...
2025/02/19 11:38:24 Move custom config...
2025/02/19 11:38:24 Upsun configuration files generated !
	OPTIONAL: Please run : "upsun app:config-validate" in order to validate them.
