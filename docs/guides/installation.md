# Installation Guide

This guide will help you install Narrative and its dependencies.

## Requirements

Narrative requires:

- Python 3.12 or higher
- NetworkX 3.2 or higher
- Pydantic 2.5 or higher

## Installation Methods

### Using pip

The simplest way to install Narrative is using pip:

```bash
pip install narrative
```

### Using Poetry

If you use Poetry for dependency management, you can add Narrative to your project:

```bash
poetry add narrative
```

### From Source

To install from source:

1. Clone the repository:

```bash
git clone https://github.com/org/narrative.git
cd narrative
```

2. Install using Poetry:

```bash
poetry install
```

Or using pip:

```bash
pip install .
```

## Optional Dependencies

Narrative has several optional dependencies for additional features:

### Visualization

For visualization features (e.g., `IDG.visualize()`), install matplotlib:

```bash
pip install narrative[visualization]
```

Or with Poetry:

```bash
poetry add narrative -E visualization
```

### OpenAI Integration

To use the OpenAI adapter for LLM rendering:

```bash
pip install narrative[openai]
```

Or with Poetry:

```bash
poetry add narrative -E openai
```

### All Optional Dependencies

To install all optional dependencies:

```bash
pip install narrative[all]
```

Or with Poetry:

```bash
poetry add narrative -E all
```

## Development Installation

For development, you'll want to install the development dependencies:

```bash
git clone https://github.com/org/narrative.git
cd narrative
poetry install --with dev,docs
```

This will install all the dependencies needed for development, testing, and building the documentation.

## Verifying Installation

To verify that Narrative is installed correctly, run:

```python
import narrative
print(narrative.__version__)
```

This should print the version number of Narrative.

## Troubleshooting

### ImportError: No module named 'narrative'

This error occurs when Python cannot find the Narrative package. Make sure you have installed it correctly and that you're using the same Python environment where you installed it.

### ImportError: No module named 'matplotlib'

This error occurs when trying to use visualization features without having matplotlib installed. Install the visualization dependencies as described above.

### ImportError: No module named 'openai'

This error occurs when trying to use the OpenAI adapter without having the OpenAI package installed. Install the OpenAI dependencies as described above.

## Next Steps

Now that you have Narrative installed, check out the [Quick Start Guide](quick-start.md) to learn how to use it.
