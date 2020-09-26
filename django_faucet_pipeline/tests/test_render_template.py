from unittest.mock import patch
from django.template import Template
from django.template.loader import get_template

from django_faucet_pipeline.templatetags.faucet_pipeline import FaucetManifestLoader


def test_renders_asset_url_to_template():
    template: Template = get_template("template.txt")
    rendered = template.render({})
    assert rendered == "foo-1234.js"


def test_renders_asset_url_even_if_manifest_is_faulty(settings):
    settings.DEBUG = True
    template: Template = get_template("template.txt")
    template.render({})
    settings.FAUCET_PIPELINE_MANIFEST = settings.FAUCET_PIPELINE_MANIFEST.replace(
        "manifest", "bad_manifest"
    )
    print(settings.FAUCET_PIPELINE_MANIFEST)
    rendered = template.render({})
    assert rendered == "foo-1234.js"


def test_no_reloads_unless_debug(settings):
    settings.DEBUG = False
    with patch(
        "django_faucet_pipeline.templatetags.faucet_pipeline.FaucetManifestLoader._instance._load_manifest",
        wraps=FaucetManifestLoader.instance()._load_manifest,
    ) as patched:
        for _ in range(0, 5):
            template: Template = get_template("template.txt")
            template.render({})
        patched.assert_not_called()


def test_reloads_with_debug(settings):
    settings.DEBUG = True
    with patch(
        "django_faucet_pipeline.templatetags.faucet_pipeline.FaucetManifestLoader._instance._load_manifest",
        wraps=FaucetManifestLoader.instance()._load_manifest,
    ) as patched:
        for _ in range(0, 5):
            template: Template = get_template("template.txt")
            template.render({})
        assert len(patched.mock_calls) == 5
