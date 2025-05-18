# Little Red Riding Hood Example

This example demonstrates how to use Narrative to create a simple narrative based on the Little Red Riding Hood story.

## Overview

The Little Red Riding Hood example shows how to:

1. Define a domain with characters, locations, intentions, and dependencies
2. Build an Intention Dependency Graph (IDG)
3. Explore and rank trajectories through the IDG
4. Render a trajectory into a natural language story
5. Visualize the IDG

## Code Example

```python
"""
Little Red Riding Hood Example

This example demonstrates how to use Narrative to create a simple narrative
based on the Little Red Riding Hood story.
"""

from narrative.core.idg_builder import IDGBuilder
from narrative.core.trajectory_explorer import TrajectoryExplorer
from narrative.llm.llm_renderer import LLMRenderer
from narrative.schemas.domain import Domain


def main() -> None:
    """Run the Little Red Riding Hood example."""
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
                "description": (
                    "Little Red must visit Grandmother to deliver the basket"
                ),
            },
            {
                "from_intention": "eat_little_red",
                "to_intention": "visit_grandmother",
                "type": "motivational",
                "description": (
                    "The Wolf wants to eat Little Red because she is visiting"
                    " Grandmother"
                ),
            },
            {
                "from_intention": "eat_grandmother",
                "to_intention": "visit_grandmother",
                "type": "motivational",
                "description": (
                    "The Wolf wants to eat Grandmother because Little Red is"
                    " visiting her"
                ),
            },
            {
                "from_intention": "rescue_little_red",
                "to_intention": "eat_little_red",
                "type": "motivational",
                "description": (
                    "The Hunter wants to rescue Little Red because the Wolf ate her"
                ),
            },
            {
                "from_intention": "rescue_grandmother",
                "to_intention": "eat_grandmother",
                "type": "motivational",
                "description": (
                    "The Hunter wants to rescue Grandmother because the Wolf ate her"
                ),
            },
            {
                "from_intention": "kill_wolf",
                "to_intention": "eat_little_red",
                "type": "motivational",
                "description": (
                    "The Hunter wants to kill the Wolf because it ate Little Red"
                ),
            },
            {
                "from_intention": "kill_wolf",
                "to_intention": "eat_grandmother",
                "type": "motivational",
                "description": (
                    "The Hunter wants to kill the Wolf because it ate Grandmother"
                ),
            },
        ],
        name="Little Red Riding Hood",
        description=(
            "A classic fairy tale about a little girl, her grandmother, and a wolf."
        ),
    )

    # Build the IDG
    print("Building the Intention Dependency Graph (IDG)...")
    idg_builder = IDGBuilder(domain)
    idg = idg_builder.build()

    # Validate the domain
    errors = idg_builder.validate()
    if errors:
        print("Domain validation errors:")
        for error in errors:
            print(f"- {error}")
        return

    # Explore trajectories
    print("Exploring trajectories...")
    explorer = TrajectoryExplorer(idg)
    trajectories = explorer.get_trajectories(max_length=7)
    print(f"Found {len(trajectories)} trajectories.")

    # Rank trajectories
    print("Ranking trajectories by drama...")
    ranked_trajectories = explorer.rank_trajectories(trajectories, metric="drama")

    # Print the top trajectory
    top_trajectory = ranked_trajectories[0]
    print("\nTop trajectory:")
    for i, intention in enumerate(top_trajectory.intentions):
        print(
            f"{i+1}. {intention['character']} intends to {intention['id']} "
            f"{intention['target']} at {intention['location']}"
        )

    # Render the story
    print("\nRendering the story...")
    renderer = LLMRenderer()  # Uses a mock LLM by default
    story = renderer.render(top_trajectory)

    # Print the story
    print("\nGenerated Story:")
    print("=" * 80)
    print(story)
    print("=" * 80)

    # Visualize the IDG (requires matplotlib)
    try:
        print("\nVisualizing the IDG...")
        idg.visualize()
    except ImportError:
        print(
            "\nMatplotlib is required for visualization. Install it with 'pip install"
            " matplotlib'."
        )


if __name__ == "__main__":
    main()
```

## Running the Example

You can run this example with:

```bash
python -m narrative.examples.little_red
```

## Expected Output

When you run the example, you should see:

1. The domain being built and validated
2. Trajectories being explored and ranked
3. The top trajectory being printed
4. A generated story based on the top trajectory
5. A visualization of the IDG (if matplotlib is installed)

## Next Steps

After exploring this example, you might want to:

- Try modifying the domain to create your own narrative
- Experiment with different metrics for ranking trajectories
- Create a custom LLM adapter for more sophisticated story generation
- Check out the [Custom Domains](custom-domains.md) and [Advanced Usage](advanced-usage.md) examples
