# Custom Domains Example

This example demonstrates how to create and use custom domains with Narrative.

## Overview

Custom domains allow you to define your own narrative worlds with unique characters, locations, intentions, and dependencies. This example shows how to:

1. Define a custom domain
2. Add custom metadata to intentions and dependencies
3. Create custom metrics for trajectory evaluation
4. Visualize and analyze your custom domain

## Creating a Custom Domain

A domain in Narrative represents a narrative world. Here's how to create a custom domain:

```python
from narrative.schemas.domain import Domain

# Define a custom domain
custom_domain = Domain(
    characters=["character1", "character2", "character3"],
    locations=["location1", "location2", "location3"],
    intentions=[
        {
            "id": "intention1",
            "character": "character1",
            "target": "character2",
            "location": "location1",
            "description": "description of intention1",
            "metadata": {
                "custom_field": "custom value",
                "priority": 1
            }
        },
        {
            "id": "intention2",
            "character": "character2",
            "target": "character3",
            "location": "location2",
            "description": "description of intention2",
            "metadata": {
                "custom_field": "another value",
                "priority": 2
            }
        },
        # Add more intentions as needed
    ],
    dependencies=[
        {
            "from_intention": "intention2",
            "to_intention": "intention1",
            "type": "intentional",
            "description": "description of dependency",
            "metadata": {
                "strength": 0.8,
                "custom_tag": "important"
            }
        },
        # Add more dependencies as needed
    ],
    name="Custom Domain Example",
    description="A custom domain for demonstration purposes."
)
```

## Adding Custom Metadata

You can add custom metadata to intentions and dependencies to store additional information:

```python
# Add custom metadata to an intention
intention = {
    "id": "custom_intention",
    "character": "character1",
    "target": "character2",
    "location": "location1",
    "description": "a custom intention",
    "metadata": {
        "emotional_intensity": 0.7,
        "time_required": "2 hours",
        "risk_level": "high",
        "tags": ["dramatic", "pivotal"]
    }
}

# Add custom metadata to a dependency
dependency = {
    "from_intention": "intention2",
    "to_intention": "intention1",
    "type": "motivational",
    "description": "a custom dependency",
    "metadata": {
        "strength": 0.9,
        "visibility": "hidden",
        "conditions": ["condition1", "condition2"],
        "probability": 0.75
    }
}
```

## Creating Custom Metrics

You can create custom metrics to evaluate trajectories according to your own criteria:

```python
from narrative.core.trajectory_explorer import MetricProtocol

class CustomMetric(MetricProtocol):
    """A custom metric for evaluating trajectories."""

    def score(self, trajectory):
        """Score a trajectory based on custom criteria."""
        score = 0

        # Example: Score based on the number of unique characters
        characters = set()
        for intention in trajectory.intentions:
            characters.add(intention["character"])
            if "target" in intention and intention["target"] in trajectory.domain.characters:
                characters.add(intention["target"])

        score += len(characters) / len(trajectory.domain.characters)

        # Example: Score based on the number of unique locations
        locations = set(intention["location"] for intention in trajectory.intentions)
        score += len(locations) / len(trajectory.domain.locations)

        # Example: Score based on custom metadata
        for intention in trajectory.intentions:
            if "metadata" in intention and "priority" in intention["metadata"]:
                score += intention["metadata"]["priority"] / 10

        return score / 3  # Normalize to [0, 1]

# Add the custom metric to the explorer
explorer.add_metric("custom", CustomMetric())

# Rank trajectories using the custom metric
ranked_trajectories = explorer.rank_trajectories(trajectories, metric="custom")
```

## Analyzing Custom Domains

You can analyze your custom domain using the built-in visualization and analysis tools:

```python
# Build the IDG
from narrative.core.idg_builder import IDGBuilder

idg_builder = IDGBuilder(custom_domain)
idg = idg_builder.build()

# Validate the domain
errors = idg_builder.validate()
if errors:
    print("Domain validation errors:")
    for error in errors:
        print(f"- {error}")

# Visualize the IDG
idg.visualize()

# Analyze the domain structure
root_intentions = idg.get_root_intentions()
leaf_intentions = idg.get_leaf_intentions()
print(f"Root intentions: {root_intentions}")
print(f"Leaf intentions: {leaf_intentions}")

# Analyze intention connectivity
for intention_id in custom_domain.get_intention_ids():
    dependencies = idg.get_dependencies(intention_id)
    dependents = idg.get_dependents(intention_id)
    print(f"Intention {intention_id}:")
    print(f"  Depends on: {dependencies}")
    print(f"  Depended on by: {dependents}")
```

## Complete Example

Here's a complete example of creating and using a custom domain:

```python
from narrative.schemas.domain import Domain
from narrative.core.idg_builder import IDGBuilder
from narrative.core.trajectory_explorer import TrajectoryExplorer, MetricProtocol
from narrative.llm.llm_renderer import LLMRenderer

# Define a custom domain
custom_domain = Domain(
    characters=["hero", "villain", "sidekick"],
    locations=["castle", "forest", "village"],
    intentions=[
        {
            "id": "rescue_sidekick",
            "character": "hero",
            "target": "sidekick",
            "location": "castle",
            "description": "from the villain's dungeon",
            "metadata": {"priority": 3, "difficulty": "high"}
        },
        {
            "id": "defeat_villain",
            "character": "hero",
            "target": "villain",
            "location": "castle",
            "description": "in an epic battle",
            "metadata": {"priority": 2, "difficulty": "high"}
        },
        {
            "id": "capture_sidekick",
            "character": "villain",
            "target": "sidekick",
            "location": "forest",
            "description": "to lure the hero",
            "metadata": {"priority": 1, "difficulty": "medium"}
        },
        {
            "id": "prepare_trap",
            "character": "villain",
            "target": "hero",
            "location": "castle",
            "description": "to capture the hero",
            "metadata": {"priority": 1, "difficulty": "low"}
        },
        {
            "id": "escape_forest",
            "character": "sidekick",
            "target": "sidekick",
            "location": "forest",
            "description": "to avoid capture",
            "metadata": {"priority": 2, "difficulty": "medium"}
        }
    ],
    dependencies=[
        {
            "from_intention": "defeat_villain",
            "to_intention": "rescue_sidekick",
            "type": "intentional",
            "description": "The hero must defeat the villain to rescue the sidekick",
            "metadata": {"strength": 0.9}
        },
        {
            "from_intention": "rescue_sidekick",
            "to_intention": "capture_sidekick",
            "type": "motivational",
            "description": "The hero wants to rescue the sidekick because the villain captured them",
            "metadata": {"strength": 0.8}
        },
        {
            "from_intention": "prepare_trap",
            "to_intention": "capture_sidekick",
            "type": "intentional",
            "description": "The villain prepares a trap after capturing the sidekick",
            "metadata": {"strength": 0.7}
        },
        {
            "from_intention": "escape_forest",
            "to_intention": "capture_sidekick",
            "type": "motivational",
            "description": "The sidekick tries to escape because the villain is trying to capture them",
            "metadata": {"strength": 0.6}
        }
    ],
    name="Hero's Journey",
    description="A classic hero's journey with a rescue mission."
)

# Define a custom metric
class DifficultyMetric(MetricProtocol):
    """A metric that scores trajectories based on difficulty."""

    def score(self, trajectory):
        """Score a trajectory based on the difficulty of its intentions."""
        difficulty_map = {"low": 0.3, "medium": 0.6, "high": 1.0}
        total_difficulty = 0

        for intention in trajectory.intentions:
            if "metadata" in intention and "difficulty" in intention["metadata"]:
                difficulty = intention["metadata"]["difficulty"]
                total_difficulty += difficulty_map.get(difficulty, 0.5)

        # Normalize by the number of intentions
        return total_difficulty / len(trajectory.intentions) if trajectory.intentions else 0

# Build the IDG
idg_builder = IDGBuilder(custom_domain)
idg = idg_builder.build()

# Explore trajectories
explorer = TrajectoryExplorer(idg)
explorer.add_metric("difficulty", DifficultyMetric())
trajectories = explorer.get_trajectories(max_length=5)

# Rank trajectories by difficulty
ranked_by_difficulty = explorer.rank_trajectories(trajectories, metric="difficulty")

# Print the top trajectory
top_trajectory = ranked_by_difficulty[0]
print("\nMost difficult trajectory:")
for i, intention in enumerate(top_trajectory.intentions):
    print(
        f"{i+1}. {intention['character']} intends to {intention['id']} "
        f"{intention['target']} at {intention['location']}"
    )

# Render the story
renderer = LLMRenderer()
story = renderer.render(top_trajectory)
print("\nGenerated Story:")
print("=" * 80)
print(story)
print("=" * 80)
```

## Next Steps

After exploring custom domains, you might want to:

- Create more complex domains with larger character and location sets
- Implement domain-specific metrics for your narrative needs
- Explore advanced trajectory generation techniques in the [Advanced Usage](advanced-usage.md) example
- Learn how to integrate custom domains with other systems
