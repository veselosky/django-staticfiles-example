"""
S3 staticfiles example settings.

This example uploads static and media files to S3 and keeps per-release
manifests by using the S3-based release-specific storage implementation.

This example places static files and media files in the same bucket. This is
not required, they may be in different buckets if desired.
"""

from .settings_shared import *  # noqa: F401,F403

# Ensure the required AWS settings are set in the environment.
BUCKET_NAME = environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY")
msg = (
    "To use S3 storage, set AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, and "
    "AWS_SECRET_ACCESS_KEY in the environment."
)
assert BUCKET_NAME and AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY, msg
# If using a CDN (you should), set the custom domain in the environment. Must
# NOT have a trailing slash.
# Example: d111111abcdef8.cloudfront.net
CDN_DOMAIN = environ.get("AWS_S3_CUSTOM_DOMAIN", None)
RELEASE_ID = environ.get("RELEASE_ID", None)
RELEASE_ID_STRATEGY = environ.get(
    "RELEASE_ID_STRATEGY", "example.release_id_strategies.git_hash"
)

STATIC_ROOT = None  # Not used with S3 storage.
if CDN_DOMAIN:
    STATIC_URL = f"https://{CDN_DOMAIN}/static/"
    MEDIA_URL = f"https://{CDN_DOMAIN}/media/"
else:
    STATIC_URL = f"https://{BUCKET_NAME}.s3.amazonaws.com/static/"
    MEDIA_URL = f"https://{BUCKET_NAME}.s3.amazonaws.com/media/"

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": BUCKET_NAME,
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "custom_domain": CDN_DOMAIN,
            "location": "media/",
        },
    },
    "staticfiles": {
        "BACKEND": "example.storages.ReleaseSpecificManifestS3Storage",
        "OPTIONS": {
            "bucket_name": BUCKET_NAME,
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "custom_domain": CDN_DOMAIN,
            "location": "static/",
            "release_id": RELEASE_ID,
            "release_id_strategy": RELEASE_ID_STRATEGY,
        },
    },
}
