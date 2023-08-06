# Github Actions

## Publish and Release

When starting a new Python project on GitHub, it's a good practice to follow a version management policy that adheres to semantic versioning, is automated, and makes it easy to maintain and understand the project's release history. One of the widely adopted version management policies for Python projects is using setuptools_scm with semantic versioning and Git tags.

To trigger the workflow `manual_release.yml` manually:

1. Go to the "Actions" tab in your GitHub repository.
2. Select the "Manual Release" workflow from the list of workflows.
3. Click the "Run workflow" button.
4. Choose the branch you want to run the workflow on, and provide the release version in the input field, like 'v0.0.5'.
5. Click the "Run workflow" button to start the workflow.

GitHub Actions will run the workflow, create a new release with the specified version, and publish it to PyPI.

The workflow `auto_release.yml` was created to automatically create a new release when a pull request with the label 'release' is merged into the main branch. 



