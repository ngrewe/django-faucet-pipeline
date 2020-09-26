import collections
import json
import logging
from pathlib import Path

from django import template
from typing import Dict, Optional

from django.apps import apps
from django.conf import settings


register = template.Library()
LOGGER = logging.getLogger("django_faucet_pipeline")


class FaucetManifestLoader:

    _manifest: Dict[str, str]

    def __init__(self):
        self._manifest = {}
        self._load_manifest()

    @property
    def manifest(self) -> Dict[str, str]:
        if settings.DEBUG:
            self._load_manifest()
        return self._manifest

    def _load_manifest(self):
        manifest_path = apps.get_app_config("django_faucet_pipeline").manifest
        try:
            with manifest_path.open("r") as fp:
                manifest = json.load(fp)
                if not isinstance(manifest, collections.abc.Mapping):
                    raise ValueError("Manifest is not a JSON object")
        except (IOError, json.JSONDecodeError, ValueError):
            LOGGER.error("Could read manifest.json", exc_info=True)
            return
        self._manifest = manifest


LOADER = FaucetManifestLoader()


@register.simple_tag()
def static_faucet(asset: str) -> Optional[str]:
    try:
        return LOADER.manifest[asset]
    except KeyError:
        LOGGER.error("Could not resolve asset %s", asset)
    return None


__all__ = ["static_faucet"]
