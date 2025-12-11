"""
This module provides some example functions to retrieve release identifiers from
different sources, such as Git and Heroku environment variables.
These identifiers can be used for versioning static files or other deployment
artifacts.
"""

import os
import subprocess
from django.conf import settings


def git_hash():
    """Get the current git commit hash."""
    try:
        git_hash = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=settings.BASE_DIR)
            .decode("utf-8")
            .strip()
        )
    except Exception:
        git_hash = "unknown"
    return git_hash


def heroku_build_commit():
    """Get the Heroku build commit hash from the environment.
    Requires the Heroku Labs feature 'runtime-dyno-build-metadata' to be enabled.
    https://devcenter.heroku.com/articles/dyno-metadata
    """
    # For Heroku, we don't always have access to the git history. We can get
    # a unique release ID from the dyno metadata. At BUILD time, Heroku sets
    # the SOURCE_VERSION environment variable to the commit hash. At RELEASE
    # time, it sets the HEROKU_BUILD_COMMIT environment variable to the same
    # value. Works as of December 2025.
    SOURCE_VERSION = os.environ.get("SOURCE_VERSION", "")
    HEROKU_BUILD_COMMIT = os.environ.get("HEROKU_BUILD_COMMIT", "")
    RELEASE_ID = os.environ.get(
        "RELEASE_ID", SOURCE_VERSION or HEROKU_BUILD_COMMIT or "unknown"
    )
    return RELEASE_ID
