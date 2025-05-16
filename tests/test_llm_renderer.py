"""
Tests for the LLM Renderer.

This module contains tests for the LLMRenderer class, which renders trajectories
into natural language stories using large language models (LLMs).
"""
# flake8: noqa: E501

from unittest.mock import MagicMock

# mypy: ignore-errors
import pytest

from narrative.core.trajectory_explorer import Trajectory
from narrative.llm.llm_renderer import LLMAdapter, LLMRenderer, MockLLMAdapter


@pytest.fixture
def simple_trajectory():
    """Create a simple trajectory for testing."""
    return Trajectory(
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
        ]
    )


@pytest.fixture
def mock_adapter():
    """Create a mock LLM adapter for testing."""
    adapter = MagicMock(spec=LLMAdapter)
    adapter.generate.return_value = "This is a test story."
    return adapter


def test_llm_renderer_initialization():
    """Test that the LLMRenderer can be initialized with an adapter."""
    # Test with default adapter
    renderer = LLMRenderer()
    assert isinstance(renderer.adapter, MockLLMAdapter)

    # Test with custom adapter
    mock_adapter = MagicMock(spec=LLMAdapter)
    renderer = LLMRenderer(adapter=mock_adapter)
    assert renderer.adapter == mock_adapter


def test_llm_renderer_render(simple_trajectory, mock_adapter):
    """Test that the LLMRenderer can render a trajectory into a story."""
    renderer = LLMRenderer(adapter=mock_adapter)
    story = renderer.render(simple_trajectory)

    # Check that the adapter was called with a prompt
    mock_adapter.generate.assert_called_once()
    prompt = mock_adapter.generate.call_args[0][0]
    assert isinstance(prompt, str)
    assert "little_red" in prompt
    assert "wolf" in prompt
    assert "grandmother" in prompt
    assert "cottage" in prompt
    assert "forest" in prompt

    # Check that the story was returned
    assert story == "This is a test story."


def test_mock_llm_adapter():
    """Test that the MockLLMAdapter returns a predefined response."""
    adapter = MockLLMAdapter()
    response = adapter.generate("This is a test prompt.")
    assert isinstance(response, str)
    assert len(response) > 0
    assert "Little Red Riding Hood" in response


def test_create_prompt(simple_trajectory):
    """Test that the LLMRenderer can create a prompt from a trajectory."""
    renderer = LLMRenderer()
    prompt = renderer._create_prompt(simple_trajectory)

    # Check that the prompt contains the intentions
    assert "1. little_red intends to visit_grandmother grandmother at cottage" in prompt
    assert "2. little_red intends to deliver_basket grandmother at cottage" in prompt
    assert "3. wolf intends to eat_little_red little_red at forest" in prompt


def test_process_response():
    """Test that the LLMRenderer can process a response from an LLM."""
    renderer = LLMRenderer()
    response = "This is a test response."
    processed_response = renderer._process_response(response)

    # For now, the response is returned as is
    assert processed_response == response


def test_llm_renderer_with_description(mock_adapter):
    """Test that the LLMRenderer can handle intentions with descriptions."""
    trajectory = Trajectory(
        intentions=[
            {
                "id": "visit_grandmother",
                "character": "little_red",
                "target": "grandmother",
                "location": "cottage",
                "description": "to bring her food",
            }
        ]
    )

    renderer = LLMRenderer(adapter=mock_adapter)
    renderer.render(trajectory)

    # Check that the adapter was called with a prompt containing the description
    prompt = mock_adapter.generate.call_args[0][0]
    assert "to bring her food" in prompt


def test_llm_renderer_with_metadata(mock_adapter):
    """Test that the LLMRenderer can handle intentions with metadata."""
    trajectory = Trajectory(
        intentions=[
            {
                "id": "visit_grandmother",
                "character": "little_red",
                "target": "grandmother",
                "location": "cottage",
                "metadata": {"time": "morning", "weather": "sunny"},
            }
        ]
    )

    renderer = LLMRenderer(adapter=mock_adapter)
    renderer.render(trajectory)

    # Check that the adapter was called with a prompt
    # (metadata is not included in the prompt by default)
    prompt = mock_adapter.generate.call_args[0][0]
    assert "visit_grandmother" in prompt
