# Advanced Usage

This guide covers advanced usage patterns and techniques for the Narrative library.

## Advanced Trajectory Generation

### Custom Trajectory Filters

You can create custom filters to select specific trajectories based on your criteria:

```python
from narrative.core.trajectory_explorer import TrajectoryExplorer

# Create a trajectory explorer
explorer = TrajectoryExplorer(idg)

# Generate all possible trajectories
all_trajectories = explorer.get_trajectories(max_length=7)

# Filter trajectories with custom criteria
def custom_filter(trajectory):
    # Example: Only include trajectories where the hero defeats the villain
    for intention in trajectory.intentions:
        if intention["id"] == "defeat_villain" and intention["character"] == "hero":
            return True
    return False

filtered_trajectories = [t for t in all_trajectories if custom_filter(t)]
print(f"Found {len(filtered_trajectories)} trajectories where the hero defeats the villain.")
```

### Trajectory Combination

You can combine multiple trajectories to create more complex narratives:

```python
from narrative.core.trajectory_explorer import Trajectory

# Assume we have two trajectories
trajectory1 = explorer.get_random_trajectory(max_length=3)
trajectory2 = explorer.get_random_trajectory(max_length=3)

# Combine trajectories (simple concatenation)
combined_intentions = trajectory1.intentions + trajectory2.intentions
combined_trajectory = Trajectory(combined_intentions, trajectory1.domain)

# Render the combined trajectory
renderer = LLMRenderer()
combined_story = renderer.render(combined_trajectory)
```

### Trajectory Manipulation

You can manipulate trajectories to create variations:

```python
# Get a trajectory
trajectory = explorer.get_random_trajectory(max_length=5)

# Remove an intention
modified_intentions = [i for i in trajectory.intentions if i["id"] != "defeat_villain"]
modified_trajectory = Trajectory(modified_intentions, trajectory.domain)

# Insert a new intention at a specific position
new_intention = {
    "id": "call_for_help",
    "character": "sidekick",
    "target": "hero",
    "location": "forest",
    "description": "to request assistance"
}
modified_intentions.insert(2, new_intention)
modified_trajectory = Trajectory(modified_intentions, trajectory.domain)

# Render the modified trajectory
modified_story = renderer.render(modified_trajectory)
```

## Advanced LLM Integration

### Custom LLM Adapters

You can create custom adapters for different LLM providers:

```python
from narrative.llm.llm_renderer import LLMAdapter

class CustomLLMAdapter(LLMAdapter):
    """A custom adapter for a specific LLM provider."""

    def __init__(self, api_key, model="default-model"):
        self.api_key = api_key
        self.model = model
        # Initialize any client libraries or connections

    def generate(self, prompt):
        """Generate text from the LLM based on the prompt."""
        # Implement the API call to your LLM provider
        # This is a placeholder implementation
        try:
            # Make API call to LLM provider
            response = self._call_llm_api(prompt)
            return response
        except Exception as e:
            print(f"Error generating text: {e}")
            return "Error generating story."

    def _call_llm_api(self, prompt):
        """Make the actual API call to the LLM provider."""
        # Implement the specific API call
        # This is a placeholder
        return f"Generated story based on prompt: {prompt[:50]}..."

# Use the custom adapter
custom_adapter = CustomLLMAdapter(api_key="your-api-key")
renderer = LLMRenderer(adapter=custom_adapter)
story = renderer.render(trajectory)
```

### Custom Prompt Templates

You can create custom prompt templates for different storytelling styles:

```python
from narrative.llm.llm_renderer import LLMRenderer

# Define custom prompt templates
fairy_tale_template = """
You are a master storyteller specializing in fairy tales.
Create a fairy tale based on the following sequence of events:

{trajectory_description}

Your fairy tale should have a clear moral lesson and use language appropriate for children.
"""

noir_template = """
You are a hardboiled detective novelist from the 1940s.
Write a noir-style narrative based on the following sequence of events:

{trajectory_description}

Use terse, cynical language with vivid descriptions of urban settings and morally ambiguous characters.
"""

sci_fi_template = """
You are a visionary science fiction author.
Create a futuristic sci-fi story based on the following sequence of events:

{trajectory_description}

Incorporate advanced technology, space travel, or other sci-fi elements while maintaining the core narrative.
"""

# Create renderers with different templates
fairy_tale_renderer = LLMRenderer(prompt_template=fairy_tale_template)
noir_renderer = LLMRenderer(prompt_template=noir_template)
sci_fi_renderer = LLMRenderer(prompt_template=sci_fi_template)

# Render the same trajectory in different styles
fairy_tale = fairy_tale_renderer.render(trajectory)
noir_story = noir_renderer.render(trajectory)
sci_fi_story = sci_fi_renderer.render(trajectory)
```

## Advanced Domain Modeling

### Dynamic Domain Generation

You can generate domains programmatically:

```python
from narrative.schemas.domain import Domain
import random

def generate_random_domain(num_characters=5, num_locations=3, num_intentions=10):
    """Generate a random domain with the specified number of elements."""
    # Generate characters
    characters = [f"character_{i}" for i in range(1, num_characters + 1)]

    # Generate locations
    locations = [f"location_{i}" for i in range(1, num_locations + 1)]

    # Generate intentions
    intentions = []
    for i in range(1, num_intentions + 1):
        character = random.choice(characters)
        target = random.choice([c for c in characters if c != character])
        location = random.choice(locations)

        intention = {
            "id": f"intention_{i}",
            "character": character,
            "target": target,
            "location": location,
            "description": f"description of intention_{i}"
        }
        intentions.append(intention)

    # Generate dependencies
    dependencies = []
    intention_ids = [intention["id"] for intention in intentions]

    # Create some random dependencies
    num_dependencies = min(len(intention_ids), num_intentions // 2)
    for _ in range(num_dependencies):
        from_intention = random.choice(intention_ids)
        to_intention = random.choice([i for i in intention_ids if i != from_intention])
        dependency_type = random.choice(["intentional", "motivational"])

        dependency = {
            "from_intention": from_intention,
            "to_intention": to_intention,
            "type": dependency_type,
            "description": f"dependency from {from_intention} to {to_intention}"
        }
        dependencies.append(dependency)

    # Create the domain
    domain = Domain(
        characters=characters,
        locations=locations,
        intentions=intentions,
        dependencies=dependencies,
        name="Randomly Generated Domain",
        description="A domain generated with random characters, locations, intentions, and dependencies."
    )

    return domain

# Generate a random domain
random_domain = generate_random_domain()

# Build an IDG from the random domain
idg_builder = IDGBuilder(random_domain)
idg = idg_builder.build()

# Validate the domain
errors = idg_builder.validate()
if errors:
    print("Domain validation errors:")
    for error in errors:
        print(f"- {error}")
else:
    print("Random domain is valid!")
```

### Domain Transformation

You can transform domains to create variations:

```python
def transform_domain(domain, transformation_type):
    """Transform a domain according to the specified transformation type."""
    # Create a copy of the domain
    transformed_domain = Domain(
        characters=domain.characters.copy(),
        locations=domain.locations.copy(),
        intentions=[intention.copy() for intention in domain.intentions],
        dependencies=[dependency.copy() for dependency in domain.dependencies],
        name=f"{domain.name} ({transformation_type})",
        description=f"{domain.description} - Transformed with {transformation_type}."
    )

    if transformation_type == "role_reversal":
        # Swap the roles of two characters
        if len(domain.characters) >= 2:
            char1, char2 = domain.characters[0], domain.characters[1]

            # Update intentions
            for intention in transformed_domain.intentions:
                if intention["character"] == char1:
                    intention["character"] = char2
                elif intention["character"] == char2:
                    intention["character"] = char1

                if intention["target"] == char1:
                    intention["target"] = char2
                elif intention["target"] == char2:
                    intention["target"] = char1

    elif transformation_type == "location_shift":
        # Change all instances of one location to another
        if len(domain.locations) >= 2:
            loc1, loc2 = domain.locations[0], domain.locations[1]

            # Update intentions
            for intention in transformed_domain.intentions:
                if intention["location"] == loc1:
                    intention["location"] = loc2

    elif transformation_type == "add_character":
        # Add a new character and some intentions
        new_character = f"new_character_{len(domain.characters) + 1}"
        transformed_domain.characters.append(new_character)

        # Add some intentions for the new character
        for i in range(2):
            target = random.choice([c for c in transformed_domain.characters if c != new_character])
            location = random.choice(transformed_domain.locations)

            new_intention = {
                "id": f"new_intention_{i+1}",
                "character": new_character,
                "target": target,
                "location": location,
                "description": f"new intention {i+1} for {new_character}"
            }
            transformed_domain.intentions.append(new_intention)

    return transformed_domain

# Transform a domain with different transformations
role_reversal_domain = transform_domain(domain, "role_reversal")
location_shift_domain = transform_domain(domain, "location_shift")
add_character_domain = transform_domain(domain, "add_character")

# Build IDGs for the transformed domains
role_reversal_idg = IDGBuilder(role_reversal_domain).build()
location_shift_idg = IDGBuilder(location_shift_domain).build()
add_character_idg = IDGBuilder(add_character_domain).build()
```

## Advanced Visualization

### Custom Visualization Styles

You can customize the visualization of IDGs:

```python
def visualize_idg_custom(idg, style="default"):
    """Visualize an IDG with custom styling."""
    import matplotlib.pyplot as plt
    import networkx as nx

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes (intentions)
    for intention_id in idg.get_intention_ids():
        intention = idg.get_intention_data(intention_id)
        G.add_node(intention_id, **intention)

    # Add edges (dependencies)
    for from_intention, to_intention in idg.get_dependency_pairs():
        dependency = idg.get_dependency_data(from_intention, to_intention)
        G.add_edge(from_intention, to_intention, **dependency)

    # Set up the figure
    plt.figure(figsize=(12, 8))

    # Apply custom styling
    if style == "character_colored":
        # Color nodes by character
        characters = idg.domain.characters
        color_map = plt.cm.get_cmap("tab10", len(characters))
        character_colors = {char: color_map(i) for i, char in enumerate(characters)}

        node_colors = [character_colors[G.nodes[node]["character"]] for node in G.nodes]

        # Create a layout
        pos = nx.spring_layout(G, seed=42)

        # Draw the graph
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
        nx.draw_networkx_edges(G, pos, edge_color="gray", arrowsize=15)
        nx.draw_networkx_labels(G, pos, font_size=10)

        # Add a legend
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w',
                          markerfacecolor=color, markersize=10, label=char)
                          for char, color in character_colors.items()]
        plt.legend(handles=legend_elements, title="Characters")

    elif style == "dependency_types":
        # Color edges by dependency type
        edge_colors = []
        for u, v in G.edges():
            if G.edges[u, v]["type"] == "intentional":
                edge_colors.append("blue")
            else:  # motivational
                edge_colors.append("red")

        # Create a layout
        pos = nx.spring_layout(G, seed=42)

        # Draw the graph
        nx.draw_networkx_nodes(G, pos, node_color="lightgray", node_size=500)
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrowsize=15)
        nx.draw_networkx_labels(G, pos, font_size=10)

        # Add a legend
        legend_elements = [
            plt.Line2D([0], [0], color='blue', lw=2, label='Intentional'),
            plt.Line2D([0], [0], color='red', lw=2, label='Motivational')
        ]
        plt.legend(handles=legend_elements, title="Dependency Types")

    else:  # default
        # Create a layout
        pos = nx.spring_layout(G, seed=42)

        # Draw the graph
        nx.draw(G, pos, with_labels=True, node_color="lightblue",
                node_size=500, edge_color="gray", arrowsize=15, font_size=10)

    plt.title(f"Intention Dependency Graph: {idg.domain.name}")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

# Visualize the IDG with different styles
visualize_idg_custom(idg, style="default")
visualize_idg_custom(idg, style="character_colored")
visualize_idg_custom(idg, style="dependency_types")
```

## Integration with Other Systems

### Saving and Loading Domains

You can save domains to JSON and load them later:

```python
import json

def save_domain_to_json(domain, filepath):
    """Save a domain to a JSON file."""
    # Convert the domain to a dictionary
    domain_dict = {
        "characters": domain.characters,
        "locations": domain.locations,
        "intentions": domain.intentions,
        "dependencies": domain.dependencies,
        "name": domain.name,
        "description": domain.description
    }

    # Write to file
    with open(filepath, "w") as f:
        json.dump(domain_dict, f, indent=2)

    print(f"Domain saved to {filepath}")

def load_domain_from_json(filepath):
    """Load a domain from a JSON file."""
    # Read from file
    with open(filepath, "r") as f:
        domain_dict = json.load(f)

    # Create a domain
    domain = Domain(
        characters=domain_dict["characters"],
        locations=domain_dict["locations"],
        intentions=domain_dict["intentions"],
        dependencies=domain_dict["dependencies"],
        name=domain_dict.get("name", "Loaded Domain"),
        description=domain_dict.get("description", "A domain loaded from JSON.")
    )

    print(f"Domain loaded from {filepath}")
    return domain

# Save a domain to JSON
save_domain_to_json(domain, "my_domain.json")

# Load a domain from JSON
loaded_domain = load_domain_from_json("my_domain.json")
```

### Web API Integration

You can create a simple web API for Narrative:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/domain", methods=["POST"])
def create_domain():
    """Create a domain from JSON data."""
    data = request.json

    try:
        domain = Domain(
            characters=data["characters"],
            locations=data["locations"],
            intentions=data["intentions"],
            dependencies=data["dependencies"],
            name=data.get("name", "API Domain"),
            description=data.get("description", "A domain created via API.")
        )

        # Build the IDG
        idg_builder = IDGBuilder(domain)
        idg = idg_builder.build()

        # Validate the domain
        errors = idg_builder.validate()
        if errors:
            return jsonify({"status": "error", "errors": errors}), 400

        # Return success
        return jsonify({"status": "success", "message": "Domain created successfully"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/trajectory", methods=["POST"])
def generate_trajectory():
    """Generate a trajectory from a domain."""
    data = request.json

    try:
        # Create the domain
        domain = Domain(
            characters=data["domain"]["characters"],
            locations=data["domain"]["locations"],
            intentions=data["domain"]["intentions"],
            dependencies=data["domain"]["dependencies"],
            name=data["domain"].get("name", "API Domain"),
            description=data["domain"].get("description", "A domain created via API.")
        )

        # Build the IDG
        idg_builder = IDGBuilder(domain)
        idg = idg_builder.build()

        # Validate the domain
        errors = idg_builder.validate()
        if errors:
            return jsonify({"status": "error", "errors": errors}), 400

        # Generate a trajectory
        explorer = TrajectoryExplorer(idg)
        max_length = data.get("max_length", 5)
        trajectory = explorer.get_random_trajectory(max_length=max_length)

        # Format the trajectory
        trajectory_data = [
            {
                "id": intention["id"],
                "character": intention["character"],
                "target": intention["target"],
                "location": intention["location"],
                "description": intention.get("description", "")
            }
            for intention in trajectory.intentions
        ]

        # Return the trajectory
        return jsonify({
            "status": "success",
            "trajectory": trajectory_data
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/story", methods=["POST"])
def generate_story():
    """Generate a story from a trajectory."""
    data = request.json

    try:
        # Create the domain
        domain = Domain(
            characters=data["domain"]["characters"],
            locations=data["domain"]["locations"],
            intentions=data["domain"]["intentions"],
            dependencies=data["domain"]["dependencies"],
            name=data["domain"].get("name", "API Domain"),
            description=data["domain"].get("description", "A domain created via API.")
        )

        # Build the IDG
        idg_builder = IDGBuilder(domain)
        idg = idg_builder.build()

        # Create a trajectory from the provided intentions
        trajectory = Trajectory(data["trajectory"], domain)

        # Render the story
        renderer = LLMRenderer()
        story = renderer.render(trajectory)

        # Return the story
        return jsonify({
            "status": "success",
            "story": story
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
```

## Next Steps

After exploring these advanced techniques, you might want to:

- Contribute to the Narrative library by adding new features or improving existing ones
- Create a custom application that uses Narrative for interactive storytelling
- Integrate Narrative with other AI systems for more sophisticated narrative generation
- Explore the [API Reference](../api/idg-engine.md) for detailed documentation on all available classes and methods
