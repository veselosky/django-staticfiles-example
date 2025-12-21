# Django Static Files Example

This is an example Django project demonstrating how Django's `staticfiles` app should be configured in production, and why.

There are four example configuration modules. Pick the settings module to use when running Django using the `--settings` option (or set `DJANGO_SETTINGS_MODULE`). Available example settings modules:

- `example.settings_default`  — Simplest static files setup using `STATIC_ROOT`.
- `example.settings_manifest` — Uses `ManifestStaticFilesStorage` for cache-busting filenames.
- `example.settings_custom`   — Custom per-release manifest storage (local filesystem).
- `example.settings_s3`       — S3-backed storage with per-release manifests.

1. Ensure you have [uv](https://astral.sh/uv/) installed.
2. From the project root, run the `collectstatic` command and pass the desired settings module. For example, to use the `custom` configuration:

   ```bash
   uv run ./manage.py collectstatic --settings=example.settings_custom --noinput
   ```

Then examine the contents of the `public/` directory to see how the static files and manifest are stored. Each example writes to a different output directory under `public/` so you can compare the results.

For simplicity of demonstration, this project has a single project-level static file, `static/example.txt`. There is a home page, and a CSS file for that page which is in the app's static files. This makes it easier to see the different outcomes of the various configurations.

## Single Server Production Configuration (per-release manifests)

For single-server (non-S3) deployments the recommended configuration is the custom per-release manifest approach (`example.settings_custom`). This uses the custom storage backend in `example/storages.py` which stores manifest files under a release-specific subdirectory so older releases continue to use their own manifests.

Run `collectstatic` with each example settings module and compare the results.

After running `collectstatic` with one or more examples and performing your comparisons:

1. Change the content of the static file at `static/example.txt`.
2. **IMPORTANT** — Commit your change to git (or set the `RELEASE_ID` environment variable to something unique).
3. Re-run `collectstatic` with each example again.

Observe how each example handles the change:

- `default`: The static file is overwritten in place. No cache busting.
- `manifest`: A new hashed file is created for the updated content; the manifest (`staticfiles.json`) is overwritten in place which can cause issues during rolling deployments or rollbacks.
- `custom`: A new hashed file and a new release-specific manifest are created; old manifests remain available for older releases.

For local testing, run the Django app and serve the `public/` directory with Python's simple HTTP server in another terminal:

```bash
uv run python -m http.server -d public/ 8080
uv run ./manage.py runserver
```

Visit `http://localhost:8000/` for the app and `http://localhost:8080/` to inspect collected static files.

## Scalable Configuration Using S3 for static files

The `example.settings_s3` module demonstrates collecting static and media files to S3 with per-release manifests. To use it, run `collectstatic` and point Django to the `example.settings_s3` module. The following environment variables are required:

- `AWS_STORAGE_BUCKET_NAME`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

Optional environment variables:

- `AWS_S3_CUSTOM_DOMAIN` — custom domain for CDN (no trailing slash).
- `RELEASE_ID` — explicit release identifier; if unset the project attempts to use the git hash.
- `RELEASE_ID_STRATEGY` — import path to a function to derive a release id (defaults to `example.release_id_strategies.git_hash`).

Example `collectstatic` using the S3 settings:

```bash
uv run ./manage.py collectstatic --settings=example.settings_s3 --noinput
```

After running `collectstatic` with `example.settings_s3`, verify files are uploaded to your S3 bucket and that `STATIC_URL` (or your `AWS_S3_CUSTOM_DOMAIN`) serves the files correctly. The output should be the same as the custom per-release manifest example, but files are stored in S3 instead of the local filesystem.
