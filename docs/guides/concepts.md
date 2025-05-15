# Core Concepts

This guide explains the core concepts behind Narrative and how they work together to create compelling narratives.

## Overview

Narrative is built around several key concepts:

1. **Domains**: The narrative world, including characters, locations, and intentions
2. **Intentions**: Goals or desires that characters have
3. **Dependencies**: Relationships between intentions
4. **Intention Dependency Graphs (IDGs)**: A graph representation of intentions and their dependencies
5. **Trajectories**: Paths through an IDG that form coherent narratives
6. **Metrics**: Ways to evaluate and rank trajectories
7. **Rendering**: Converting trajectories into natural language stories using LLMs

Let's explore each of these concepts in more detail.

## Domains

A domain represents a narrative world with characters, locations, intentions, and dependencies. It's the foundation of any narrative created with NarrativeIDG.

```python
from narrative import Domain

domain = Domain(
    characters=["little_red", "wolf", "grandmother", "hunter"],
    locations=["forest", "cottage", "village"],
    intentions=[...],
    dependencies=[...],
    name="Little Red Riding Hood",
    description="A classic fairy tale about a little girl, her grandmother, and a wolf."
)
```

A domain must have at least one character, one location, and one intention. Dependencies are optional but are usually necessary to create interesting narratives.

## Intentions

An intention represents a character's goal or desire. It's defined by:

- An ID (a unique identifier)
- A character (who has the intention)
- A target (usually another character)
- A location (where the intention takes place)
- An optional description
- Optional metadata

```python
{
    "id": "visit_grandmother",
    "character": "little_red",
    "target": "grandmother",
    "location": "cottage",
    "description": "to check on her health"
}
```

Intentions are the building blocks of narratives. They represent what characters want to do and why they want to do it.

## Dependencies

A dependency represents a relationship between two intentions. It's defined by:

- A from_intention (the intention that depends on another)
- A to_intention (the intention that is depended upon)
- A type (intentional or motivational)
- An optional description
- Optional metadata

```python
{
    "from_intention": "deliver_basket",
    "to_intention": "visit_grandmother",
    "type": "intentional",
    "description": "Little Red must visit Grandmother to deliver the basket"
}
```

There are two types of dependencies:

- **Intentional**: The from_intention is a sub-goal of the to_intention. For example, "deliver_basket" is a sub-goal of "visit_grandmother".
- **Motivational**: The from_intention is motivated by the to_intention. For example, "eat_little_red" is motivated by "visit_grandmother" (the wolf wants to eat Little Red because she is visiting her grandmother).

## Intention Dependency Graphs (IDGs)

An Intention Dependency Graph (IDG) is a directed graph where nodes represent intentions and edges represent dependencies between intentions. It's built from a domain using the IDGBuilder class.

```python
from narrative import IDGBuilder

idg_builder = IDGBuilder(domain)
idg = idg_builder.build()
```

The IDG provides methods for working with the graph, such as:

- `get_root_intentions()`: Get intentions that are not depended upon by any other intention
- `get_leaf_intentions()`: Get intentions that do not depend on any other intention
- `get_intention_data(intention_id)`: Get the data associated with an intention
- `get_dependency_data(from_intention, to_intention)`: Get the data associated with a dependency
- `visualize()`: Visualize the IDG using matplotlib

## Trajectories

A trajectory is a path through an IDG that forms a coherent narrative. It's a sequence of intentions that can be rendered into a natural language story.

Trajectories are generated using the TrajectoryExplorer class:

```python
from narrative import TrajectoryExplorer

explorer = TrajectoryExplorer(idg)
trajectories = explorer.get_trajectories(max_length=5)
```

The `get_trajectories()` method generates all possible trajectories through the IDG up to a maximum length. You can also generate a random trajectory using the `get_random_trajectory()` method.

## Metrics

Metrics are used to evaluate and rank trajectories according to different criteria. Narrative includes several built-in metrics:

- **Novelty**: Measures the diversity of characters, locations, and intention types
- **Coherence**: Measures the continuity of characters and locations between adjacent intentions
- **Drama**: Measures the presence of conflict, character arcs, and emotional intensity

You can rank trajectories using these metrics:

```python
ranked_trajectories = explorer.rank_trajectories(trajectories, metric="drama")
```

You can also create custom metrics by implementing a class with a `score()` method:

```python
class LengthMetric:
    def score(self, trajectory):
        return len(trajectory.intentions)

explorer.add_metric("length", LengthMetric())
ranked_by_length = explorer.rank_trajectories(trajectories, metric="length")
```

## Rendering

Rendering is the process of converting a trajectory into a natural language story using a large language model (LLM). NarrativeIDG includes the LLMRenderer class for this purpose:

```python
from narrative import LLMRenderer

renderer = LLMRenderer()
story = renderer.render(trajectory)
```

By default, the LLMRenderer uses a mock LLM that returns a predefined story. You can use a real LLM by creating a custom adapter:

```python
from narrative.llm.llm_renderer import OpenAIAdapter

adapter = OpenAIAdapter(api_key="your-api-key-here")
renderer = LLMRenderer(adapter=adapter)
```

You can also create your own adapter by implementing the LLMAdapter interface:

```python
from narrative.llm.llm_renderer import LLMAdapter

class MyAdapter(LLMAdapter):
    def generate(self, prompt):
        # Your implementation here
        return "Generated story"

renderer = LLMRenderer(adapter=MyAdapter())
```

## Putting It All Together

Here's how these concepts work together to create a narrative:

1. You define a domain with characters, locations, intentions, and dependencies.
2. The IDGBuilder builds an IDG from the domain.
3. The TrajectoryExplorer generates trajectories through the IDG.
4. You rank the trajectories using metrics to find the most interesting ones.
5. The LLMRenderer renders a trajectory into a natural language story.

This process combines symbolic planning (the IDG and trajectories) with natural language generation (the LLM) to create compelling narratives that are both coherent and engaging.

## Next Steps

Now that you understand the core concepts of Narrative, you can:

- Follow the [Quick Start Guide](quick-start.md) to create your first narrative
- Explore the [API Reference](../api/idg-engine.md) for detailed documentation
- Check out more examples in the [Examples](../examples/little-red.md) section
