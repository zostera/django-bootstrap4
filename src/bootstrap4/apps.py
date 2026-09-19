"""Application configuration and system checks."""

from django.apps import AppConfig
from django.core.checks import Warning, register

#: Settings that existed once, with the hint that makes this worth more than "unknown key".
REMOVED_SETTINGS = {
    "base_url": "dropped in 0.0.8, use `css_url` and `javascript_url`",
}


@register()
def check_bootstrap4_settings(app_configs, **kwargs):
    """Warn about keys in the BOOTSTRAP4 setting that this package never reads."""
    from django.conf import settings

    from bootstrap4.bootstrap import BOOTSTRAP4_DEFAULTS

    warnings = []
    for key in getattr(settings, "BOOTSTRAP4", {}):
        if key in BOOTSTRAP4_DEFAULTS:
            continue
        hint = REMOVED_SETTINGS.get(key, "not a django-bootstrap4 setting; it is ignored")
        warnings.append(
            Warning(
                f"BOOTSTRAP4[{key!r}] has no effect: {hint}.",
                id="bootstrap4.W001",
            )
        )
    return warnings


class Bootstrap4Config(AppConfig):
    """Default application configuration."""

    name = "bootstrap4"
