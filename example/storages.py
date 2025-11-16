import subprocess

from django.conf import settings
from django.contrib.staticfiles.storage import (
    ManifestStaticFilesStorage,
    StaticFilesStorage,
)

# To ensure a unique name across deployments, get the hash for the current git commit
# and use it as a prefix for the static files manifest. This way, even if the static 
# files are collected to the same STATIC_ROOT location, the manifest files will be 
# different for each deployment. Calculated at import time so that running processes 
# will not be affected by changes in the working directory.
try:
    GIT_HASH = (
        subprocess.check_output(["git", "rev-parse", "HEAD"])
        .decode("utf-8")
        .strip()
    )
except Exception:
    GIT_HASH = "unknown"


# Custom static files storage that stores the manifest file in a unique subdirectory.
# NOTE: This example uses the local filesystem for storage. If you're using S3Storage
# from django-storages, subclass from S3ManifestStaticStorage instead.
class ExampleManifestLocalStorage(ManifestStaticFilesStorage):
    def __init__(self, *args, **kwargs):
        # Override the storage location for the manifest file to be in a subdirectory
        # named after the release ID (or git hash). This prevents cross-talk between 
        # releases during deployments or rollbacks.
        release_id = kwargs.pop("release_id", None)
        if not release_id:  # In case the key is set but None/empty
            release_id = GIT_HASH
        manifest_storage = StaticFilesStorage(location=settings.STATIC_ROOT / release_id)
        super().__init__(*args, manifest_storage=manifest_storage, **kwargs)
