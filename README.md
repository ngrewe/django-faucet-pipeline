# Django Faucet Pipeline

[![Build Status](https://dev.azure.com/glaux/update-broker/_apis/build/status/ngrewe.django-faucet-pipeline?repoName=ngrewe%2Fdjango-faucet-pipeline&branchName=main)](https://dev.azure.com/glaux/update-broker/_build/latest?definitionId=8&repoName=ngrewe%2Fdjango-faucet-pipeline&branchName=main)

django-faucet-pipeline integrates [faucet-pipeline](https://www.faucet-pipeline.org) with Django. It allows you to
transparently reference assets created by faucet-pipeline in Django templates and operate on them using the [django.contrib.staticfiles](https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/) app.

## Usage

### Configuring Django and faucet-pipeline

To start using faucet-pipeline in Django, you need to make sure that both the staticfiles and the django_faucet_pipeline app are mentioned in the `INSTALLED_APPS` section of `settings.py`:

```py
INSTALLED_APPS = [
    …,
    'django.contrib.staticfiles',
    'django_faucet_pipeline',
]
```

faucet-pipeline needs to be configured to write a `manifest.json` file for integrating with Django. By default,
django-faucet-pipeline will look for this file in the `BASE_DIR` of the Django project (as specified
by `settings.py`). You can customise the search path using `FAUCET_PIPELINE_MANIFEST` setting.

The manifest configuration needs to align with the Django configuration in two
respects: The `STATIC_URL` in settings by needs to be the same as the `baseURI` in the manifest config.
Also, all assets need to be output into the `webRoot`, which also needs to be configured as one of the
`STATICFILES_DIRS` in Django. For example, if you were to have the following configuration in Django:

```py
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "dist/"
]
```

A compatible `faucet.config.js` might look as follows:

```js
module.exports = {
    js: {
        input: 'app/index.js',
        output: 'dist/bundle.js'
    },
    manifest: {
        target: "./manifest.json",
        key: "short",
        baseURI: "/static/",
        webRoot: "./dist"
    }
};
```

django-faucet-pipeline will emit an error message if it cannot read the manifest file, but it will not check
whether your webRoot and and `STATICFILES_DIRS` configuration is correct.

### Referencing assets

In order to reference an asset, you simply use the `static_faucet` template tag from the `faucet_pipeline`
library. This behaves similarly to the "standard" `static` tag, but automatically expands the canonical name
of the asset to the current (potentially fingerprinted) name.

```html
{% load static_faucet from faucet_pipeline %}
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Hello World</title>
  </head>
  <body> 
  <div id="container"></div>
  <script src="{% static_faucet "bundle.js" %}" type="text/javascript"></script>
  </body>
</html>
```

### Debug vs. Production

The behaviour of django-faucet-pipeline will change depending on whether the Django settings `DEBUG` is set
to true or not. If debug mode is enabled, the manifest file will be re-read when ever a template is rendered.
In production, you should have `DEBUG` set to `False`, in which case manifest.json will be read once on first
access and then cached indefinitely.