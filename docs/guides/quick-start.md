# Quick Start Guide

This guide will help you get started with Narrative by walking through a simple example.

## Installation

First, make sure you have Narrative installed:

```bash
pip install narrative
```

For more installation options, see the [Installation Guide](installation.md).

## Basic Usage

Let's create a simple narrative based on the Little Red Riding Hood story.

### 1. Define the Domain

First, we need to define the narrative domain with characters, locations, intentions, and dependencies:

```python
from narrative import Domain, IDGBuilder, TrajectoryExplorer, LLMRenderer

# Define the domain
domain = Domain(
    characters=["little_red", "wolf", "grandmother", "hunter"],
    locations=["forest", "cottage", "village"],
    intentions=[
        {
            "id": "visit_grandmother",
            "character": "little_red",
            "target": "grandmother",
            "location": "cottage",
            "description": "to check on her health",
        },
        {
            "id": "deliver_basket",
            "character": "little_red",
            "target": "grandmother",
            "location": "cottage",
            "description": "containing food and medicine",
        },
        {
            "id": "eat_little_red",
            "character": "wolf",
            "target": "little_red",
            "location": "forest",
            "description": "after tricking her",
        },
        {
            "id": "eat_grandmother",
            "character": "wolf",
            "target": "grandmother",
            "location": "cottage",
            "description": "after disguising as Little Red",
        },
        {
            "id": "rescue_little_red",
            "character": "hunter",
            "target": "little_red",
            "location": "cottage",
            "description": "from the wolf's stomach",
        },
        {
            "id": "rescue_grandmother",
            "character": "hunter",
            "target": "grandmother",
            "location": "cottage",
            "description": "from the wolf's stomach",
        },
        {
            "id": "kill_wolf",
            "character": "hunter",
            "target": "wolf",
            "location": "cottage",
            "description": "to save Little Red and Grandmother",
        },
    ],
    dependencies=[
        {
            "from_intention": "deliver_basket",
            "to_intention": "visit_grandmother",
            "type": "intentional",
            "description": "Little Red must visit Grandmother to deliver the basket",
        },
        {
            "from_intention": "eat_little_red",
            "to_intention": "visit_grandmother",
            "type": "motivational",
            "description": "The Wolf wants to eat Little Red because she is visiting Grandmother",
        },
        {
            "from_intention": "eat_grandmother",
            "to_intention": "visit_grandmother",
            "type": "motivational",
            "description": "The Wolf wants to eat Grandmother because Little Red is visiting her",
        },
        {
            "from_intention": "rescue_little_red",
            "to_intention": "eat_little_red",
            "type": "motivational",
            "description": "The Hunter wants to rescue Little Red because the Wolf ate her",
        },
        {
            "from_intention": "rescue_grandmother",
            "to_intention": "eat_grandmother",
            "type": "motivational",
            "description": "The Hunter wants to rescue Grandmother because the Wolf ate her",
        },
        {
            "from_intention": "kill_wolf",
            "to_intention": "eat_little_red",
            "type": "motivational",
            "description": "The Hunter wants to kill the Wolf because it ate Little Red",
        },
        {
            "from_intention": "kill_wolf",
            "to_intention": "eat_grandmother",
            "type": "motivational",
            "description": "The Hunter wants to kill the Wolf because it ate Grandmother",
        },
    ],
    name="Little Red Riding Hood",
    description="A classic fairy tale about a little girl, her grandmother, and a wolf.",
)
```

### 2. Build the Intention Dependency Graph (IDG)

Next, we build an IDG from the domain:

```python
# Build the IDG
idg_builder = IDGBuilder(domain)
idg = idg_builder.build()

# Validate the domain
errors = idg_builder.validate()
if errors:
    print("Domain validation errors:")
    for error in errors:
        print(f"- {error}")
```

### 3. Explore Trajectories

Now we can explore possible trajectories through the IDG:

```python
# Create a trajectory explorer
explorer = TrajectoryExplorer(idg)

# Generate all possible trajectories up to length 7
trajectories = explorer.get_trajectories(max_length=7)
print(f"Found {len(trajectories)} trajectories.")

# Rank trajectories by drama
ranked_trajectories = explorer.rank_trajectories(trajectories, metric="drama")

# Print the top trajectory
top_trajectory = ranked_trajectories[0]
print("\nTop trajectory:")
for i, intention in enumerate(top_trajectory.intentions):
    print(
        f"{i+1}. {intention['character']} intends to {intention['id']} "
        f"{intention['target']} at {intention['location']}"
    )
```

### 4. Render a Story

Finally, we can render the trajectory into a natural language story:

```python
# Create a renderer (uses a mock LLM by default)
renderer = LLMRenderer()

# Render the story
story = renderer.render(top_trajectory)
print("\nGenerated Story:")
print("=" * 80)
print(story)
print("=" * 80)
```

### 5. Visualize the IDG

If you have matplotlib installed, you can visualize the IDG:

```python
# Visualize the IDG
idg.visualize()
```

## Using a Custom LLM

By default, Narrative uses a mock LLM that returns a predefined story. To use a real LLM like OpenAI's GPT models, you can create a custom adapter:

```python
from narrative.llm.llm_renderer import OpenAIAdapter

# Create an OpenAI adapter
adapter = OpenAIAdapter(api_key="your-api-key-here")

# Create a renderer with the custom adapter
renderer = LLMRenderer(adapter=adapter)

# Render the story
story = renderer.render(top_trajectory)
```

## Creating Custom Metrics

You can create custom metrics to rank trajectories according to your own criteria:

```python
class LengthMetric:
    """A metric that scores trajectories based on length."""
    
    def score(self, trajectory):
        """Score a trajectory based on length."""
        return len(trajectory.intentions)

# Add the custom metric to the explorer
explorer.add_metric("length", LengthMetric())

# Rank trajectories by length
ranked_by_length = explorer.rank_trajectories(trajectories, metric="length")
```

## Next Steps

Now that you've seen the basics of Narrative, you can:

- Learn more about the core concepts in the [Concepts Guide](concepts.md)
- Explore the [API Reference](../api/idg-engine.md) for detailed documentation
- Check out more examples in the [Examples](../examples/little-red.md) section
- Learn how to [generate documentation and use GitHub CI](documentation.md) for contributing to the project
