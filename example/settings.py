"""
Compatibility wrapper settings for the example project.

This file acts as the legacy default `example.settings` module. It
imports the real settings from the per-example module for the "default"
example. To select a different staticfiles example, pass Django a
different settings module via the `--settings` option (or set
`DJANGO_SETTINGS_MODULE`). For example:

  ./manage.py collectstatic --settings=example.settings_custom --noinput

Available example settings modules:

- `example.settings_default`  -- default STATIC_ROOT-based setup
- `example.settings_manifest` -- ManifestStaticFilesStorage example
- `example.settings_custom`   -- custom per-release-manifest (local)
- `example.settings_s3`       -- S3-based storage with per-release manifests

By default this module simply loads the `default` example so existing
invocations that rely on `example.settings` will retain the previous
behavior.
"""

from .settings_default import *  # noqa: F401,F403

