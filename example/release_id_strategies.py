"""
This module provides some example functions to retrieve release identifiers from 
different sources, such as Git and Heroku environment variables.
These identifiers can be used for versioning static files or other deployment
artifacts.
"""
import os
import subprocess


def git_hash():
    """Get the current git commit hash."""
    try:
        git_hash = (
            subprocess.check_output(["git", "rev-parse", "HEAD"])
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
    return os.environ.get("HEROKU_BUILD_COMMIT", "unknown")
