"""
Default staticfiles example settings.

Import everything common from `settings_shared` and then set the
minimal staticfiles settings required for the "default" example.
"""

from .settings_shared import *  # noqa: F401,F403

STATIC_ROOT = BASE_DIR / "public" / "static-default"
MEDIA_ROOT = BASE_DIR / "public" / "media"
STATIC_URL = "http://localhost:8080/static-default/"
MEDIA_URL = "http://localhost:8080/media/"

# For demonstration, create the STATIC_ROOT directory if it doesn't exist.
if STATIC_ROOT:
    STATIC_ROOT.mkdir(parents=True, exist_ok=True)
