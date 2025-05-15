"""
Tests for the IDG Builder.

This module contains tests for the IDGBuilder class, which builds an Intention Dependency Graph (IDG)
from a domain.
"""

import pytest
import networkx as nx

from narrative.schemas.domain import Domain, Intention, Dependency
from narrative.core.idg_builder import IDGBuilder, IDG


def test_idg_builder_initialization():
    """Test that the IDGBuilder can be initialized with a domain."""
    domain = Domain(
        characters=["little_red", "wolf", "grandmother", "hunter"],
        locations=["forest", "cottage", "village"],
        intentions=[
            {
                "id": "visit_grandmother",
                "character": "little_red",
                "target": "grandmother",
                "location": "cottage",
            }
        ],
        dependencies=[],
    )
    
    builder = IDGBuilder(domain)
    assert builder.domain == domain


def test_idg_builder_build():
    """Test that the IDGBuilder can build an IDG from a domain."""
    domain = Domain(
        characters=["little_red", "wolf", "grandmother", "hunter"],
        locations=["forest", "cottage", "village"],
        intentions=[
            {
                "id": "visit_grandmother",
                "character": "little_red",
                "target": "grandmother",
                "location": "cottage",
            },
            {
                "id": "deliver_basket",
                "character": "little_red",
                "target": "grandmother",
                "location": "cottage",
            },
        ],
        dependencies=[
            {
                "from_intention": "deliver_basket",
                "to_intention": "visit_grandmother",
                "type": "intentional",
            }
        ],
    )
    
    builder = IDGBuilder(domain)
    idg = builder.build()
    
    assert isinstance(idg, IDG)
    assert len(idg.nodes) == 2
    assert len(idg.edges) == 1
    assert "visit_grandmother" in idg.nodes
    assert "deliver_basket" in idg.nodes
    assert ("deliver_basket", "visit_grandmother") in idg.edges


def test_idg_builder_validate():
    """Test that the IDGBuilder can validate a domain."""
    # Valid domain
    domain = Domain(
        characters=["little_red", "wolf", "grandmother", "hunter"],
        locations=["forest", "cottage", "village"],
        intentions=[
            {
                "id": "visit_grandmother",
                "character": "little_red",
                "target": "grandmother",
                "location": "cottage",
            }
        ],
        dependencies=[],
    )
    
    builder = IDGBuilder(domain)
    errors = builder.validate()
    assert len(errors) == 0
    
    # Invalid domain with non-existent character
    domain = Domain(
        characters=["little_red", "wolf", "grandmother", "hunter"],
        locations=["forest", "cottage", "village"],
        intentions=[
            {
                "id": "visit_grandmother",
                "character": "non_existent_character",
                "target": "grandmother",
                "location": "cottage",
            }
        ],
        dependencies=[],
    )
    
    builder = IDGBuilder(domain)
    errors = builder.validate()
    assert len(errors) == 1
    assert "non_existent_character" in errors[0]
    
    # Invalid domain with non-existent location
    domain = Domain(
        characters=["little_red", "wolf", "grandmother", "hunter"],
        locations=["forest", "cottage", "village"],
        intentions=[
            {
                "id": "visit_grandmother",
                "character": "little_red",
                "target": "grandmother",
                "location": "non_existent_location",
            }
        ],
        dependencies=[],
    )
    
    builder = IDGBuilder(domain)
    errors = builder.validate()
    assert len(errors) == 1
    assert "non_existent_location" in errors[0]
    
    # Invalid domain with non-existent intention in dependency
    domain = Domain(
        characters=["little_red", "wolf", "grandmother", "hunter"],
        locations=["forest", "cottage", "village"],
        intentions=[
            {
                "id": "visit_grandmother",
                "character": "little_red",
                "target": "grandmother",
                "location": "cottage",
            }
        ],
        dependencies=[
            {
                "from_intention": "non_existent_intention",
                "to_intention": "visit_grandmother",
                "type": "intentional",
            }
        ],
    )
    
    builder = IDGBuilder(domain)
    errors = builder.validate()
    assert len(errors) == 1
    assert "non_existent_intention" in errors[0]


def test_idg_methods():
    """Test the methods of the IDG class."""
    domain = Domain(
        characters=["little_red", "wolf", "grandmother", "hunter"],
        locations=["forest", "cottage", "village"],
        intentions=[
            {
                "id": "visit_grandmother",
                "character": "little_red",
                "target": "grandmother",
                "location": "cottage",
            },
            {
                "id": "deliver_basket",
                "character": "little_red",
                "target": "grandmother",
                "location": "cottage",
            },
            {
                "id": "eat_little_red",
                "character": "wolf",
                "target": "little_red",
                "location": "forest",
            },
        ],
        dependencies=[
            {
                "from_intention": "deliver_basket",
                "to_intention": "visit_grandmother",
                "type": "intentional",
            },
            {
                "from_intention": "eat_little_red",
                "to_intention": "visit_grandmother",
                "type": "motivational",
            },
        ],
    )
    
    builder = IDGBuilder(domain)
    idg = builder.build()
    
    # Test get_root_intentions
    root_intentions = idg.get_root_intentions()
    assert len(root_intentions) == 1
    assert "visit_grandmother" in root_intentions
    
    # Test get_leaf_intentions
    leaf_intentions = idg.get_leaf_intentions()
    assert len(leaf_intentions) == 2
    assert "deliver_basket" in leaf_intentions
    assert "eat_little_red" in leaf_intentions
    
    # Test get_intention_data
    intention_data = idg.get_intention_data("visit_grandmother")
    assert intention_data["character"] == "little_red"
    assert intention_data["target"] == "grandmother"
    assert intention_data["location"] == "cottage"
    
    # Test get_dependency_data
    dependency_data = idg.get_dependency_data("deliver_basket", "visit_grandmother")
    assert dependency_data["type"] == "intentional"
