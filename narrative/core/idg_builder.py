"""
IDG Builder

This module contains the IDGBuilder class, which builds an Intention Dependency
Graph (IDG) from a domain.
"""
# flake8: noqa: E501

from typing import Any, Dict, List, Set, Tuple

import networkx as nx

from narrative.schemas.domain import Dependency, Domain, Intention


class IDG(nx.DiGraph):
    """
    Intention Dependency Graph (IDG) class.

    An IDG is a directed graph where nodes represent intentions and edges
    represent dependencies between intentions. This class extends
    networkx.DiGraph to provide additional methods for working with IDGs.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize an IDG."""
        super().__init__(*args, **kwargs)

    def get_root_intentions(self) -> Set[str]:
        """
        Get the root intentions in the IDG.

        Root intentions are intentions that are not depended upon by any other
        intention.

        Returns:
            A set of intention IDs that are roots in the IDG.
        """
        return {node for node in self.nodes if self.in_degree(node) == 0}

    def get_leaf_intentions(self) -> Set[str]:
        """
        Get the leaf intentions in the IDG.

        Leaf intentions are intentions that do not depend on any other
        intention.

        Returns:
            A set of intention IDs that are leaves in the IDG.
        """
        return {node for node in self.nodes if self.out_degree(node) == 0}

    def get_intention_data(self, intention_id: str) -> Dict[str, Any]:
        """
        Get the data associated with an intention.

        Args:
            intention_id: The ID of the intention.

        Returns:
            A dictionary containing the intention data.

        Raises:
            KeyError: If the intention ID is not in the IDG.
        """
        return dict(self.nodes[intention_id])

    def get_dependency_data(
        self, from_intention: str, to_intention: str
    ) -> Dict[str, Any]:
        """
        Get the data associated with a dependency.

        Args:
            from_intention: The ID of the intention that depends on another.
            to_intention: The ID of the intention that is depended upon.

        Returns:
            A dictionary containing the dependency data.

        Raises:
            KeyError: If the dependency is not in the IDG.
        """
        return dict(self.edges[from_intention, to_intention])

    def visualize(
        self,
        figsize: Tuple[int, int] = (12, 8),
        node_size: int = 2000,
        font_size: int = 10,
        edge_width: int = 2,
        edge_color: str = "black",
        node_color: str = "lightblue",
        with_labels: bool = True,
    ) -> None:
        """
        Visualize the IDG using matplotlib.

        Args:
            figsize: The figure size (width, height) in inches.
            node_size: The size of the nodes.
            font_size: The font size for the node labels.
            edge_width: The width of the edges.
            edge_color: The color of the edges.
            node_color: The color of the nodes.
            with_labels: Whether to display node labels.

        Raises:
            ImportError: If matplotlib is not installed.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError as err:
            raise ImportError(
                "Matplotlib is required for visualization. "
                "Install it with 'pip install matplotlib'."
            ) from err

        plt.figure(figsize=figsize)
        pos = nx.spring_layout(self, seed=42)
        nx.draw(
            self,
            pos,
            with_labels=with_labels,
            node_size=node_size,
            font_size=font_size,
            width=edge_width,
            edge_color=edge_color,
            node_color=node_color,
        )

        # Add edge labels for dependency types
        edge_labels = {(u, v): self.edges[u, v]["type"] for u, v in self.edges}
        nx.draw_networkx_edge_labels(self, pos, edge_labels=edge_labels)

        plt.axis("off")
        plt.tight_layout()
        plt.show()


class IDGBuilder:
    """
    Builder class for creating Intention Dependency Graphs (IDGs) from domains.
    """

    def __init__(self, domain: Domain):
        """
        Initialize an IDGBuilder with a domain.

        Args:
            domain: The domain to build an IDG from.
        """
        self.domain = domain

    def build(self) -> IDG:
        """
        Build an IDG from the domain.

        Returns:
            An IDG representing the domain.
        """
        idg = IDG()

        # Add nodes (intentions)
        for intention_obj in self.domain.intentions:
            # Convert to Intention if it's a dict
            if isinstance(intention_obj, dict):
                intention = Intention(**intention_obj)
            else:
                intention = intention_obj

            # Create node attributes
            node_attrs = {
                "character": intention.character,
                "target": intention.target,
                "location": intention.location,
                "description": intention.description,
                "metadata": intention.metadata,
            }

            # Add node with intention data
            idg.add_node(intention.id, **node_attrs)

        # Add edges (dependencies)
        for dependency_obj in self.domain.dependencies:
            # Convert to Dependency if it's a dict
            if isinstance(dependency_obj, dict):
                dependency = Dependency(**dependency_obj)
            else:
                dependency = dependency_obj

            # Create edge attributes
            edge_attrs = {
                "type": dependency.type,
                "description": dependency.description,
                "metadata": dependency.metadata,
            }

            # Add edge with dependency data
            idg.add_edge(
                dependency.from_intention, dependency.to_intention, **edge_attrs
            )

        return idg

    def validate(self) -> List[str]:
        """
        Validate the domain.

        This method checks that all characters, locations, and intentions
        referenced in the domain
        actually exist.

        Returns:
            A list of validation error messages. If the list is empty,
            the domain is valid.
        """
        errors: List[str] = []

        # Check that all characters referenced in intentions exist
        for intention_obj in self.domain.intentions:
            # Convert to Intention if it's a dict
            if isinstance(intention_obj, dict):
                intention = Intention(**intention_obj)
            else:
                intention = intention_obj

            if intention.character not in self.domain.characters:
                errors.append(
                    f"Character '{intention.character}' missing (id: {intention.id})."
                )

            if intention.target not in self.domain.characters:
                errors.append(
                    f"Target '{intention.target}' missing (id: {intention.id})."
                )

        # Check that all locations referenced in intentions exist
        for intention_obj in self.domain.intentions:
            # Convert to Intention if it's a dict
            if isinstance(intention_obj, dict):
                intention = Intention(**intention_obj)
            else:
                intention = intention_obj

            if intention.location not in self.domain.locations:
                errors.append(
                    f"Location '{intention.location}' missing (id: {intention.id})."
                )

        # Check that all intentions referenced in dependencies exist
        intention_ids = set()
        for intention_obj in self.domain.intentions:
            if isinstance(intention_obj, dict):
                intention_ids.add(intention_obj["id"])
            else:
                intention_ids.add(intention_obj.id)

        for dependency_obj in self.domain.dependencies:
            # Convert to Dependency if it's a dict
            if isinstance(dependency_obj, dict):
                dependency = Dependency(**dependency_obj)
            else:
                dependency = dependency_obj

            if dependency.from_intention not in intention_ids:
                errors.append(f"From-intention '{dependency.from_intention}' missing.")

            if dependency.to_intention not in intention_ids:
                errors.append(f"To-intention '{dependency.to_intention}' missing.")

        return errors
