"""
Custom staticfiles example settings.

This example uses the project's custom storage class which stores per-release
manifest files in a subdirectory named by the release id.
"""

from .settings_shared import *  # noqa: F401,F403

STATIC_ROOT = BASE_DIR / "public" / "static-manifest-custom"
# Set STATIC_URL as appropriate for your deployment. Here we default to a
# localhost URL for dev/test.
STATIC_URL = environ.get("STATIC_URL", "http://localhost:8080/static-manifest-custom/")

RELEASE_ID = environ.get("RELEASE_ID", None)
RELEASE_ID_STRATEGY = environ.get(
    "RELEASE_ID_STRATEGY", "example.release_id_strategies.git_hash"
)

STORAGES = {
    "default": {  # location defaults to MEDIA_ROOT
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "example.storages.ReleaseSpecificManifestLocalStorage",
        "OPTIONS": {  # location defaults to STATIC_ROOT
            "release_id": RELEASE_ID,
            "release_id_strategy": RELEASE_ID_STRATEGY,
        },
    },
}
# For demonstration only, create the STATIC_ROOT directory if it doesn't exist.
if STATIC_ROOT:
    STATIC_ROOT.mkdir(parents=True, exist_ok=True)
