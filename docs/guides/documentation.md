# Documentation Guide

This guide explains how to generate documentation using MkDocs and how to use the GitHub CI workflow for automatic documentation deployment.

## Setting Up MkDocs Locally

### Prerequisites

Before you can generate documentation, make sure you have:

1. Python 3.12 or later installed
2. Poetry installed (see [Installation Guide](installation.md))
3. The project cloned to your local machine

### Installing Documentation Dependencies

The documentation dependencies are defined in the `pyproject.toml` file under the `[tool.poetry.group.docs.dependencies]` section. To install them, run:

```bash
poetry install --with docs
```

This will install MkDocs, the Material theme, and other plugins required for building the documentation.

### Building Documentation Locally

To build the documentation locally, run:

```bash
poetry run mkdocs build
```

This will generate the static site in the `site` directory. You can open the `site/index.html` file in your browser to view the documentation.

### Serving Documentation Locally

For development purposes, you can serve the documentation locally with live reloading:

```bash
poetry run mkdocs serve
```

This will start a local server at http://127.0.0.1:8000/ where you can preview the documentation as you make changes.

## Documentation Structure

The documentation is organized as follows:

- `docs/`: Contains all the documentation source files
  - `index.md`: The home page
  - `guides/`: User guides and tutorials
  - `api/`: API reference documentation
  - `examples/`: Example usage and code snippets

The navigation structure is defined in the `mkdocs.yml` file under the `nav` section.

## Adding New Documentation

To add new documentation:

1. Create a new Markdown file in the appropriate directory
2. Add the file to the navigation structure in `mkdocs.yml`
3. Build and preview the documentation locally
4. Commit and push your changes

## Using the GitHub CI Workflow

The project includes a GitHub CI workflow that automatically builds and deploys the documentation when changes are pushed to the main branch.

### How the CI Workflow Works

The workflow is defined in `.github/workflows/docs-build.yml` and consists of two jobs:

1. `build`: Builds the documentation and uploads it as an artifact
2. `deploy`: Deploys the documentation to GitHub Pages (only on the main branch)

The workflow is triggered when:
- Changes are pushed to the main branch that affect documentation files
- A pull request is opened or updated that affects documentation files
- The workflow is manually triggered

### Setting Up GitHub Pages for the First Time

To set up GitHub Pages for your documentation:

1. Go to your repository on GitHub
2. Navigate to Settings > Pages
3. Under "Source", select "GitHub Actions"
4. Make sure your repository has the appropriate permissions for GitHub Actions

### Manually Triggering the Workflow

You can manually trigger the documentation build and deploy workflow:

1. Go to your repository on GitHub
2. Navigate to Actions > Build and Deploy Documentation
3. Click "Run workflow"
4. Select the branch to run the workflow on
5. Click "Run workflow"

### Troubleshooting CI Issues

If the CI workflow fails, check the following:

1. Make sure all documentation dependencies are correctly specified in `pyproject.toml`
2. Verify that the documentation builds successfully locally
3. Check the workflow logs for specific error messages
4. Ensure that the repository has the necessary permissions for GitHub Actions

## Best Practices for Documentation

- Keep documentation up-to-date with code changes
- Use clear, concise language
- Include code examples where appropriate
- Use admonitions (notes, warnings, tips) to highlight important information
- Add diagrams or images to explain complex concepts
- Test documentation locally before pushing changes
- Review documentation in pull requests

## Generating API Reference Documentation

The API reference documentation is generated automatically from docstrings using the `mkdocstrings` plugin. To ensure your API is well-documented:

1. Write comprehensive docstrings for all public classes, methods, and functions
2. Use Google-style docstrings, as configured in `mkdocs.yml`
3. Include type hints in your code
4. Run `poetry run mkdocs build --strict` to check for documentation errors
