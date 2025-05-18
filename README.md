# Narrative

**A Python library that marries symbolic planning with large language models (LLMs) to create compelling narratives.**

[![PyPI version](https://img.shields.io/pypi/v/narrative.svg)](https://pypi.org/project/narrative/)
[![Python Version](https://img.shields.io/pypi/pyversions/narrative.svg)](https://pypi.org/project/narrative/)
[![License](https://img.shields.io/pypi/l/narrative.svg)](https://github.com/org/narrative/blob/main/LICENSE)
[![CI](https://github.com/albinks/narrative/actions/workflows/ci.yml/badge.svg)](https://github.com/albinks/narrative/actions/workflows/ci.yml)
[![Documentation](https://github.com/albinks/narrative/actions/workflows/docs-build.yml/badge.svg)](https://github.com/albinks/narrative/actions/workflows/docs-build.yml)

## Overview

Narrative is an open-source Python library that combines symbolic planning with large language models (LLMs) to keep interactive narratives coherent, reactive, and designer-friendly.

It transforms domain definitions into Intention Dependency Graphs (IDGs), serves up exemplar story branches in milliseconds, and hands those skeletons to an LLM to render rich prose or dialogue.

This library is based on the research presented in [this AAAI paper](https://cdn.aaai.org/ojs/12989/12989-52-16506-1-2-20201228.pdf), which introduces the concept of Intention Dependency Graphs for narrative generation.

## Features

- **Domain Modeling**: Define narrative domains with characters, locations, intentions, and dependencies
- **Intention Dependency Graphs**: Build and visualize graphs of narrative intentions and their dependencies
- **Trajectory Exploration**: Generate and rank possible narrative trajectories through the IDG
- **LLM Rendering**: Convert trajectories into natural language stories using LLMs
- **Extensible Architecture**: Create custom metrics, adapters, and visualizations

## Installation

```bash
pip install narrative
```

For more installation options, see the [Installation Guide](https://org.github.io/narrative/guides/installation/).

## Quick Example

```python
from narrative import Domain, IDGBuilder, TrajectoryExplorer, LLMRenderer

# Define a simple domain based on Little Red Riding Hood
domain = Domain(
    characters=["little_red", "wolf", "grandmother", "hunter"],
    locations=["forest", "cottage", "village"],
    intentions=[
        {"id": "visit_grandmother", "character": "little_red", "target": "grandmother", "location": "cottage"},
        {"id": "deliver_basket", "character": "little_red", "target": "grandmother", "location": "cottage"},
        {"id": "eat_little_red", "character": "wolf", "target": "little_red", "location": "forest"},
        {"id": "eat_grandmother", "character": "wolf", "target": "grandmother", "location": "cottage"},
        {"id": "rescue_little_red", "character": "hunter", "target": "little_red", "location": "cottage"},
        {"id": "rescue_grandmother", "character": "hunter", "target": "grandmother", "location": "cottage"},
        {"id": "kill_wolf", "character": "hunter", "target": "wolf", "location": "cottage"}
    ],
    dependencies=[
        {"from_intention": "deliver_basket", "to_intention": "visit_grandmother", "type": "intentional"},
        {"from_intention": "eat_little_red", "to_intention": "visit_grandmother", "type": "motivational"},
        {"from_intention": "eat_grandmother", "to_intention": "visit_grandmother", "type": "motivational"},
        {"from_intention": "rescue_little_red", "to_intention": "eat_little_red", "type": "motivational"},
        {"from_intention": "rescue_grandmother", "to_intention": "eat_grandmother", "type": "motivational"},
        {"from_intention": "kill_wolf", "to_intention": "eat_little_red", "type": "motivational"},
        {"from_intention": "kill_wolf", "to_intention": "eat_grandmother", "type": "motivational"}
    ]
)

# Build IDG
idg_builder = IDGBuilder(domain)
idg = idg_builder.build()

# Explore trajectories
explorer = TrajectoryExplorer(idg)
trajectories = explorer.get_trajectories(max_length=7)
ranked_trajectories = explorer.rank_trajectories(trajectories, metric="novelty")

# Render story
renderer = LLMRenderer()
story = renderer.render(ranked_trajectories[0])

print(story)
```

## Documentation

For full documentation, visit [org.github.io/narrative](https://org.github.io/narrative).

- [Installation Guide](https://org.github.io/narrative/guides/installation/)
- [Quick Start Guide](https://org.github.io/narrative/guides/quick-start/)
- [Core Concepts](https://org.github.io/narrative/guides/concepts/)
- [API Reference](https://org.github.io/narrative/api/idg-engine/)
- [Examples](https://org.github.io/narrative/examples/little-red/)

## Why Narrative?

### For Game Developers

- Create coherent, branching narratives that respond to player choices
- Ensure narrative consistency while allowing for emergent storytelling
- Generate rich prose and dialogue from simple narrative structures

### For Researchers

- Experiment with hybrid symbolic-neural approaches to narrative generation
- Study the interaction between planning and natural language generation
- Develop and test new metrics for narrative quality

### For Writers

- Explore alternative narrative paths and "what if" scenarios
- Generate story outlines and drafts based on character intentions
- Experiment with different narrative structures and dependencies

## Development Setup

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management

### Setting up the development environment

1. Clone the repository:
   ```bash
   git clone https://github.com/org/narrative.git
   cd narrative
   ```

2. Install dependencies:
   ```bash
   poetry install --with dev
   ```

3. Install pre-commit hooks:
   ```bash
   poetry run pre-commit install
   ```

Pre-commit will now run automatically on every commit to ensure code quality. The hooks include:
- black (code formatting)
- mypy (static type checking)
- ruff (linting)
- isort (import sorting)
- commitizen (commit message formatting and version checking)

You can also run the hooks manually on all files:
```bash
poetry run pre-commit run --all-files
```

## Versioning

Narrative follows [Semantic Versioning](https://semver.org/) (SemVer). Version numbers follow the format `MAJOR.MINOR.PATCH`:

- **MAJOR** version increases when incompatible API changes are made
- **MINOR** version increases when functionality is added in a backward-compatible manner
- **PATCH** version increases when backward-compatible bug fixes are made

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages to automate version management and changelog generation. Each commit message should be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types include:
- `feat`: A new feature (increments MINOR version)
- `fix`: A bug fix (increments PATCH version)
- `docs`: Documentation changes only
- `style`: Changes that don't affect code meaning (formatting, etc.)
- `refactor`: Code changes that neither fix bugs nor add features
- `perf`: Performance improvements
- `test`: Adding or correcting tests
- `build`: Changes to build system or dependencies
- `ci`: Changes to CI configuration
- `chore`: Other changes that don't modify src or test files

Breaking changes should be indicated by adding `!` after the type/scope or by adding a footer `BREAKING CHANGE: description`. This will increment the MAJOR version.

Example:
```
feat(idg): add support for conditional dependencies

This adds the ability to define dependencies that only activate under certain conditions.

BREAKING CHANGE: The dependency format in the Domain class has changed to accommodate conditions.
```

### Version Management

Versioning is managed using [Commitizen](https://commitizen-tools.github.io/commitizen/). The current version is maintained in both `pyproject.toml` and `narrative/__init__.py`.

To bump the version based on your commits:
```bash
poetry run cz bump
```

This will:
1. Determine the new version based on commit types since the last tag
2. Update version numbers in all configured files
3. Create a new commit with the version change
4. Create a new tag
5. Update the CHANGELOG.md file

For more details, see the [CHANGELOG.md](CHANGELOG.md) file.

## Contributing

Contributions are welcome! To contribute:

1. Clone the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

For more details, see the [Contributing Guide](https://org.github.io/narrative/contributing/).

## License

Narrative is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Citation

If you use Narrative in your research, please cite it as:

```bibtex
@software{narrative2025,
  author = {Narrative Contributors},
  title = {Narrative: A Python library for narrative generation},
  year = {2025},
  url = {https://github.com/org/narrative},
}
```

Please also cite the original research paper that this library is based on:

```bibtex
@inproceedings{idg2020,
  title = {Intention Dependency Graphs for Interactive Narrative Generation},
  author = {Paper Authors},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence},
  year = {2020},
  url = {https://cdn.aaai.org/ojs/12989/12989-52-16506-1-2-20201228.pdf}
}
```
