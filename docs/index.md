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

For more installation options, see the [Installation Guide](guides/installation.md).

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

## Getting Started

- [Installation Guide](guides/installation.md): How to install Narrative
- [Quick Start Guide](guides/quick-start.md): Create your first narrative
- [Core Concepts](guides/concepts.md): Learn about the key concepts behind Narrative

## Contributing

Contributions are welcome! See the [Contributing Guide](contributing.md) for more information.

## License

Narrative is licensed under the MIT License. See the [LICENSE](https://github.com/org/narrative/blob/main/LICENSE) file for more information.

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
