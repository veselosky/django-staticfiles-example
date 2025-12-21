"""
Manifest staticfiles example settings.

This example uses Django's `ManifestStaticFilesStorage` which writes a
`staticfiles.json` manifest into `STATIC_ROOT`. Because the manifest is
overwritten on each `collectstatic` run, this setup is only suitable
for deployments where each release has its own separate `STATIC_ROOT`
directory (e.g., per-release containers or per-release directories on
a shared host).
"""

from .settings_shared import *  # noqa: F401,F403

STATIC_ROOT = BASE_DIR / "public" / "static-manifest-default"
# Set STATIC_URL as appropriate for your deployment. Here we default to a
# localhost URL for dev/test.
STATIC_URL = environ.get("STATIC_URL", "http://localhost:8080/static-manifest-default/")

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}
# For demonstration only, create the STATIC_ROOT directory if it doesn't exist.
if STATIC_ROOT:
    STATIC_ROOT.mkdir(parents=True, exist_ok=True)
