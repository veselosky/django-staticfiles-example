# Django Static Files Example

This is an example Django project demonstrating how Django's `staticfiles` app should be configured in production, and why.

There are four example configurations, which can be selected by setting the `STATIC_CONFIG` environment variable to one of the following values:

- `default`: Simplest static files setup, providing only `STATIC_ROOT` setting, leaving STORAGES to the default. This setup does not provide cache busting for static files or atomic deployments. It is NOT recommended for production use.
- `manifest`: Uses `ManifestStaticFilesStorage` to provide cache busting by appending a hash to static file names. The manifest file is stored in `STATIC_ROOT/staticfiles.json`. This setup provides cache busting but may have issues during rolling deployments or rollbacks due to the manifest being overwritten. Only suitable for production if your deployment process is "stop-update-start" (your site will be down briefly during deployment) or if you can tolerate some strange behavior during deployment.
- `custom`: A custom static files storage backend that stores the manifest file in a unique subdirectory based on the deployment's release ID or git hash. Old manifest files are retained. This prevents issues with manifest files cross-talk during rolling deployments or rollbacks. See `example/storages.py` for implementation details (it's very simple).
- `s3`: Uses `django-storages` to collect static files to Amazon S3 with per-release manifests.

1. Ensure you have [uv](https://astral.sh/uv/) installed.
2. From the project root, run the `collectstatic` command with the desired static files configuration. For example, to use the `custom` configuration:

   ```bash
   STATIC_CONFIG=custom uv run ./manage.py collectstatic --noinput
   ```

Then examine the contents of the `public/` directory to see how the static files and manifest are stored. Each config writes to a different output directory under `public/` to make it easy to compare their outputs.

For simplicity of demonstration, this project has a single project-level static file, `static/example.txt`. There is a home page, and a CSS file for that page which is in the app's static files. This makes it easier to see the different outcomes of the various configurations. 

## Single Server Production Configuration (`STATIC_CONFIG=custom`)
For single server production deployments (non-S3), the recommended configuration is `STATIC_CONFIG=custom`, which uses the custom storage backend defined in `example/storages.py`. This backend stores manifest files in a unique subdirectory based on the deployment's release ID or git hash, preventing issues during rolling deployments or rollbacks.

Run `collectstatic` with each configuration and compare the results.

After running `collectstatic` with all three configurations and performing your comparisons:

1. Change the content of the static file at `static/example.txt` 
2. **IMPORTANT** — Commit your change to git (or set the RELEASE_ID environment variable to something unique). 
3. Re-run `collectstatic` with each configuration again. 
 
Observe how each configuration handles the change.

- `default`: The static file is overwritten in place. No cache busting.
- `manifest`: The static file `example.txt` is overwritten, but the old hashed file, `example.d78029940deb.txt`, is still there with the original content. A new hashed file has been created with the latest content. The manifest file is overwritten in place, and only lists the new hashed file. This may cause issues during rolling deployments or rollbacks. Processes running the old code may read the new manifest file and get the wrong hashed file names.
- `custom`: The static file `example.txt` is overwritten, but the old hashed file, `example.d78029940deb.txt`, is still there with the original content. A new hashed file has been created with the latest content. A new manifest file is stored in a new subdirectory named after the current git hash (or RELEASE_ID). The old manifest file is still present in its own subdirectory. This prevents issues during rolling deployments or rollbacks. Code will always read the correct manifest file for its own release.

However, when you run the development server with `uv run ./manage.py runserver`, you will find your static files are not being served. This is because DEBUG is set to False in `settings.py` for production-like settings, and `staticfiles` does not serve static files when DEBUG is False. In a production environment, you would typically serve static files using a web server like Nginx or Apache, or through a CDN. For this test, we'll use Python's built-in HTTP server. 

Open another terminal window and run:

```bash
uv run python -m http.server -d public/ 8080
```

Now you have Django serving your application on port 8000 and a simple HTTP server serving your static files on port 8080. You can access your application at `http://localhost:8000/` and verify that the static files are being served correctly from `http://localhost:8080/static/`.

## Scalable Configuration Using S3 for static files (`STATIC_CONFIG=s3`)

This project also includes an example configuration for serving static files from Amazon S3 with per-release manifests. To enable it, set `STATIC_CONFIG=s3` and provide the required AWS environment variables.

- Required environment variables:
   - `AWS_STORAGE_BUCKET_NAME` — the S3 bucket name to store media and static files.
   - `AWS_ACCESS_KEY_ID` — AWS access key ID with permissions to the bucket.
   - `AWS_SECRET_ACCESS_KEY` — AWS secret access key.

- Optional environment variables:
   - `STATIC_URL` — custom CDN or S3 URL to serve static files from (must end with `/`). If not provided, the default is `https://<BUCKET_NAME>.s3.amazonaws.com/static/`. (See `example/settings.py`)
   - `AWS_S3_CUSTOM_DOMAIN` — custom domain (e.g., CloudFront distribution domain) for S3 URLs (do NOT include a trailing slash).
   - `RELEASE_ID` — optional explicit release identifier. If not set, the project attempts to use the git hash of the current commit.
   - `RELEASE_ID_STRATEGY` — import path to a function used to derive a release id; defaults to `example.release_id_strategies.git_hash`. See `example/release_id_strategies.py` for other examples.

- Notes:
   - When using `STATIC_CONFIG=s3`, `STATIC_ROOT` is not used (set to `None`). Static files are uploaded directly to S3.
   - The example storage backend used is `example.storages.ReleaseSpecificManifestS3Storage`, which stores per-release manifest files under the configured S3 `location` so different releases don't overwrite each other's manifest.

- Example `collectstatic` command (bash):

   ```bash
   STATIC_CONFIG=s3 \
      AWS_STORAGE_BUCKET_NAME=your-bucket \
      AWS_ACCESS_KEY_ID=AKIA... \
      AWS_SECRET_ACCESS_KEY=... \
      uv run ./manage.py collectstatic --noinput
   ```

After running `collectstatic` with `STATIC_CONFIG=s3`, verify files are uploaded to your S3 bucket and that the generated `STATIC_URL` (or your `AWS_S3_CUSTOM_DOMAIN`) serves the files correctly.
