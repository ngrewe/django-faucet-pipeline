import collections
import json
from pathlib import Path

from django.apps import AppConfig, apps
from django.conf import settings
from django.core.checks import register, Tags, Error
from django.utils.translation import gettext_lazy as _


class FaucetPipelineConfig(AppConfig):

    name = "django_faucet_pipeline"
    verbose_name = _("Faucet Pipeline")

    @property
    def manifest(self) -> Path:
        return Path(
            getattr(settings, "FAUCET_PIPELINE_MANIFEST", None)
            or Path(getattr(settings, "BASE_DIR", "") or "") / "manifest.json"
        )


@register(Tags.templates)
def check_manifest(app_configs, **kwargs):
    config: FaucetPipelineConfig
    for app_config in app_configs or [apps.get_app_config("django_faucet_pipeline")]:
        if isinstance(app_config, FaucetPipelineConfig):
            config = app_config
            break
    else:
        return []
    manifest: Path = config.manifest
    if not manifest.is_file():
        return [
            Error(
                _("Faucet pipeline manifest does not exist"),
                hint=_(
                    "Check FAUCET_PIPELINE_MANIFEST setting or faucet configuration"
                ),
                obj=manifest,
                id="django_faucet_pipeline.E001",
            )
        ]
    try:
        with manifest.open("r") as fp:
            obj = json.load(fp)
            if not isinstance(obj, collections.abc.Mapping):
                raise ValueError("Not a mapping")
    except (json.JSONDecodeError, ValueError):
        return [
            Error(
                _("Faucet pipeline manifest is not a valid JSON object"),
                obj=manifest,
                id="django_faucet_pipeline.E002",
            )
        ]
    return []
