# Contributing to Narrative

Thank you for your interest in contributing to Narrative! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and considerate of others when participating in discussions, submitting issues, or contributing code.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- Git

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/narrative.git
   cd narrative
   ```
3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
4. Set up pre-commit hooks:
   ```bash
   poetry run pre-commit install
   ```

## Development Workflow

### Creating a Branch

Create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

Use a descriptive branch name that reflects the changes you're making.

### Making Changes

1. Make your changes to the codebase
2. Add tests for your changes
3. Run the tests to ensure they pass:
   ```bash
   poetry run pytest
   ```
4. Update documentation as needed

### Committing Changes

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages. This helps us generate changelogs and versioning automatically.

Format your commit messages as follows:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Types include:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Changes that do not affect the meaning of the code (formatting, etc.)
- `refactor`: Code changes that neither fix a bug nor add a feature
- `perf`: Performance improvements
- `test`: Adding or correcting tests
- `chore`: Changes to the build process or auxiliary tools

Example:
```
feat(idg): add support for custom intention types

This commit adds support for custom intention types in the IDG builder.
The Domain class now accepts a custom_intention_types parameter.

Closes #123
```

### Submitting a Pull Request

1. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Go to the original repository on GitHub and create a pull request
3. Fill out the pull request template with details about your changes
4. Wait for a maintainer to review your pull request

## Testing

We use pytest for testing. All new code should include appropriate tests.

Run the tests with:

```bash
poetry run pytest
```

For coverage reports:

```bash
poetry run pytest --cov=narrative
```

## Documentation

We use MkDocs with the Material theme for documentation. Documentation is written in Markdown and stored in the `docs/` directory.

### Building Documentation

Build the documentation with:

```bash
poetry run mkdocs build
```

Serve the documentation locally with:

```bash
poetry run mkdocs serve
```

Then visit `http://localhost:8000` to view the documentation.

### API Documentation

API documentation is generated automatically from docstrings using mkdocstrings. Please follow the Google docstring style for all functions and classes:

```python
def example_function(param1, param2):
    """Short description of the function.

    Longer description explaining the function in more detail.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of the return value

    Raises:
        ExceptionType: When and why this exception is raised
    """
    # Function implementation
```

## Code Style

We follow the [Black](https://black.readthedocs.io/) code style and use [isort](https://pycqa.github.io/isort/) for import sorting. These are enforced by pre-commit hooks.

Additionally, we use [flake8](https://flake8.pycqa.org/) for linting and [mypy](https://mypy.readthedocs.io/) for type checking.

Run the style checks with:

```bash
poetry run pre-commit run --all-files
```

## Release Process

Releases are managed by the maintainers. We follow semantic versioning (SemVer) for version numbers.

## Getting Help

If you need help with contributing, please:

1. Check the documentation
2. Look for similar issues on the issue tracker
3. Open a new issue with your question

## Thank You

Your contributions are greatly appreciated! By contributing to Narrative, you're helping to make it a better tool for everyone.
