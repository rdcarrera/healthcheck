config_template_require = {
    "module": "str",
    "mysql_conf": {
        "port": 0,
        "host": "str",
        "database": "str",
        "user": "str",
        "password": "str",
        "raise_on_warnings": True
    }
}
config_template_optional = {
    "mysql_table": {
        "table": "str",
        "conditional": "str"
    }
}