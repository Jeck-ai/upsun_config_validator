# schema.py
UPSUN_SCHEMA = {
    "type": "object",
    "properties": {
        "applications": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "pattern": "^(nodejs|php|python|golang|ruby|java|dotnet|static|clojure|elixir|rust|bun|perl|sbcl|perlcgi|phpcgi)@[0-9]+\\.[0-9]+$"
                    },
                    "stack": {
                        "type": "array",
                        "items": {
                            "oneOf": [
                                {"type": "string"},
                                {
                                    "type": "object",
                                    "patternProperties": {
                                        "^(php|python|nodejs|ruby|java|golang|dotnet|clojure|elixir|rust|bun|perl|sbcl)$": {
                                            "type": "object",
                                            "properties": {
                                                "extensions": {"type": "array", "items": {"type": "string"}}
                                            }
                                        }
                                    },
                                    "additionalProperties": false
                                }
                            ]
                        }
                    },
                    "web": {
                        "type": "object",
                        "properties": {
                            "commands": {
                                "type": "object",
                                "additionalProperties": {"type": "string"}
                            },
                            "locations": {
                                "type": "object",
                                "additionalProperties": {
                                    "type": "object",
                                    "properties": {
                                        "root": {"type": "string"},
                                        "index": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        },
                                        "passthru": {"type": ["string", "boolean"]},
                                        "allow": {"type": "boolean"},
                                        "scripts": {"type": "boolean"},
                                        "expires": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "hooks": {
                        "type": "object",
                        "properties": {
                            "build": {"type": "string"},
                            "deploy": {"type": "string"},
                            "post_deploy": {"type": "string"}
                        }
                    },
                    "relationships": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "object",
                            "properties": {
                                "service": {"type": "string"},
                                "endpoint": {"type": "string"}
                            },
                            "required": ["service"]
                        }
                    },
                    "mounts": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "object",
                            "properties": {
                                "source": {"type": "string"},
                                "source_path": {"type": "string"}
                            },
                            "required": ["source"]
                        }
                    },
                    "dependencies": {
                        "type": "object",
                        "properties": {
                            "python3": {"type": "object"},
                            "nodejs": {"type": "object"}, 
                            "php": {"type": "object"}
                        }
                    },
                    "commands": {
                        "type": "object",
                        "additionalProperties": {"type": "string"}
                    }
                },
                "oneOf": [
                    {"required": ["type"]},
                    {"required": ["stack"]}
                ]
            }
        },
        "services": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "pattern": "^(mariadb|mysql|postgresql|redis|memcached|rabbitmq|solr|elasticsearch|mongodb|influxdb|kafka|varnish|rust):[0-9]+\\.[0-9]+$"
                    },
                    "configuration": {
                        "type": "object",
                        "properties": {
                            "schema": {"type": "string"},
                            "extensions": {"type": "array", "items": {"type": "string"}},
                            "vcl": {"type": "string"}
                        }
                    },
                    "relationships": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "object",
                            "properties": {
                                "service": {"type": "string"},
                                "endpoint": {"type": "string"}
                            },
                            "required": ["service"]
                        }
                    }
                },
                "required": ["type"]
            }
        },
        "routes": {
            "type": "object",
            "patternProperties": {
                "^https?://(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*\\{default\\}/?.*$": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "enum": ["upstream", "redirect"]},
                        "upstream": {"type": "string"},
                        "to": {"type": "string"},
                        "cache": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean"},
                                "default_ttl": {"type": "integer"},
                                "cookies": {"type": "array", "items": {"type": "string"}},
                                "headers": {"type": "array", "items": {"type": "string"}}
                            }
                        },
                        "ssi": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean"}
                            }
                        }
                    },
                    "required": ["type"],
                    "oneOf": [
                        {
                            "properties": {"type": {"const": "upstream"}},
                            "required": ["upstream"]
                        },
                        {
                            "properties": {"type": {"const": "redirect"}},
                            "required": ["to"]
                        }
                    ]
                }
            },
            "additionalProperties": false
        }
    },
    "required": ["applications"],
    "additionalProperties": false
}
