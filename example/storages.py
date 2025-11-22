import os.path
from django.conf import settings
from django.contrib.staticfiles.storage import (
    ManifestStaticFilesStorage,
    StaticFilesStorage,
)
from django.utils.module_loading import import_string

from storages.backends.s3 import S3StaticStorage, S3ManifestStaticStorage


# Custom static files storage that stores the manifest file in a unique subdirectory.
class ReleaseSpecificManifestLocalStorage(ManifestStaticFilesStorage):
    def __init__(self, *args, **kwargs):
        # Determine the release ID to use for the manifest file location.
        release_id = kwargs.pop("release_id", None)
        release_id_strategy_path = kwargs.pop("release_id_strategy", None)
        if not release_id:
            release_id_strategy = import_string(release_id_strategy_path)
            release_id = release_id_strategy()
        # Set up the manifest storage to use a subdirectory named after the release ID.
        manifest_storage = StaticFilesStorage(location=settings.STATIC_ROOT / release_id)
        super().__init__(*args, manifest_storage=manifest_storage, **kwargs)


class ReleaseSpecificManifestS3Storage(S3ManifestStaticStorage):
    def __init__(self, *args, **kwargs):
        # Determine the release ID to use for the manifest file location.
        release_id = kwargs.pop("release_id", None)
        release_id_strategy_path = kwargs.pop("release_id_strategy", None)
        if not release_id:
            release_id_strategy = import_string(release_id_strategy_path)
            release_id = release_id_strategy()

        # Set up the manifest storage to use a subdirectory named after the release ID
        # otherwise using all the same S3 settings as the main storage.
        opts = kwargs.copy() # copy to avoid modifying original
        opts["location"] = os.path.join(kwargs.get("location", ""), release_id)
        manifest_storage = S3StaticStorage(**opts)
        super().__init__(*args, manifest_storage=manifest_storage, **kwargs)
