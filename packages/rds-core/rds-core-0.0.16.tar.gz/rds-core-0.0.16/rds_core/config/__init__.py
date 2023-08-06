"""
Documentar.
"""

import dynaconf

settings = dynaconf.Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.yaml", "settings.toml", ".secrets.toml"],
)
