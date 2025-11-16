# Django Static Files Example

This is an example Django project demonstrating how Django's `staticfiles` app should be configured in production, and why.

For simplicity of demonstration, this project has a single project-level static file, `static/example.txt`. This makes it easier to see the different outcomes of the various configurations.

There are three example configurations, which can be selected by setting the `STATIC_CONFIG` environment variable to one of the following values:

- `default`: Simplest static files setup, providing only `STATIC_ROOT` setting, leaving STORAGES to the default. This setup does not provide cache busting for static files or atomic deployments. It is NOT recommended for production use.
- `manifest`: Uses `ManifestStaticFilesStorage` to provide cache busting by appending a hash to static file names. The manifest file is stored in `STATIC_ROOT/staticfiles.json`. This setup provides cache busting but may have issues during rolling deployments or rollbacks due to the manifest being overwritten. Only suitable for production if your deployment process is "stop-update-start" (your site will be down briefly during deployment) or if you can tolerate some strange behavior during deployment.
- `custom`: **RECOMMENDED** — A custom static files storage backend that stores the manifest file in a unique subdirectory based on the deployment's release ID or git hash. Old manifest files are retained. This prevents issues with manifest files cross-talk during rolling deployments or rollbacks. See `example/storages.py` for implementation details (it's very simple).

## Usage

1. Ensure you have [uv](https://astral.sh/uv/) installed.
2. From the project root, run the `collectstatic` command with the desired static files configuration. For example, to use the recommended `custom` configuration:

   ```bash
   STATIC_CONFIG=custom uv run ./manage.py collectstatic --noinput
   ```

Then examine the contents of the `public/` directory to see how the static files and manifest are stored. Each config writes to a different output directory under `public/` to make it easy to compare their outputs.

After running `collectstatic` with all three configurations and performing your comparisons:

1. Change the content of the static file at `static/example.txt` 
2. **IMPORTANT** — Commit your change to git (or set the RELEASE_ID environment variable to something unique). 
3. Re-run `collectstatic` with each configuration again. 
 
Observe how each configuration handles the change.

- `default`: The static file is overwritten in place. No cache busting.
- `manifest`: The static file `example.txt` is overwritten, but the old hashed file, `example.d78029940deb.txt`, is still there with the original content. A new hashed file has been created with the latest content. The manifest file is overwritten in place, and only lists the new hashed file. This may cause issues during rolling deployments or rollbacks. Processes running the old code may read the new manifest file and get the wrong hashed file names.
- `custom`: The static file `example.txt` is overwritten, but the old hashed file, `example.d78029940deb.txt`, is still there with the original content. A new hashed file has been created with the latest content. A new manifest file is stored in a new subdirectory named after the current git hash (or RELEASE_ID). The old manifest file is still present in its own subdirectory. This prevents issues during rolling deployments or rollbacks. Code will always read the correct manifest file for its own release.
