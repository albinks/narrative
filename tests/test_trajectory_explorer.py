"""
Tests for the Trajectory Explorer.

This module contains tests for the TrajectoryExplorer class, which generates and ranks trajectories
through an Intention Dependency Graph (IDG).
"""

import pytest

from narrative.schemas.domain import Domain
from narrative.core.idg_builder import IDGBuilder
from narrative.core.trajectory_explorer import (
    TrajectoryExplorer,
    Trajectory,
    NoveltyMetric,
    CoherenceMetric,
    DramaMetric,
)


@pytest.fixture
def simple_domain():
    """Create a simple domain for testing."""
    return Domain(
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
            {
                "id": "eat_grandmother",
                "character": "wolf",
                "target": "grandmother",
                "location": "cottage",
            },
            {
                "id": "rescue_little_red",
                "character": "hunter",
                "target": "little_red",
                "location": "cottage",
            },
            {
                "id": "rescue_grandmother",
                "character": "hunter",
                "target": "grandmother",
                "location": "cottage",
            },
            {
                "id": "kill_wolf",
                "character": "hunter",
                "target": "wolf",
                "location": "cottage",
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
            {
                "from_intention": "eat_grandmother",
                "to_intention": "visit_grandmother",
                "type": "motivational",
            },
            {
                "from_intention": "rescue_little_red",
                "to_intention": "eat_little_red",
                "type": "motivational",
            },
            {
                "from_intention": "rescue_grandmother",
                "to_intention": "eat_grandmother",
                "type": "motivational",
            },
            {
                "from_intention": "kill_wolf",
                "to_intention": "eat_little_red",
                "type": "motivational",
            },
            {
                "from_intention": "kill_wolf",
                "to_intention": "eat_grandmother",
                "type": "motivational",
            },
        ],
    )


@pytest.fixture
def simple_idg(simple_domain):
    """Create a simple IDG for testing."""
    builder = IDGBuilder(simple_domain)
    return builder.build()


@pytest.fixture
def explorer(simple_idg):
    """Create a TrajectoryExplorer for testing."""
    return TrajectoryExplorer(simple_idg)


def test_trajectory_explorer_initialization(simple_idg):
    """Test that the TrajectoryExplorer can be initialized with an IDG."""
    explorer = TrajectoryExplorer(simple_idg)
    assert explorer.idg == simple_idg
    assert "novelty" in explorer.metrics
    assert "coherence" in explorer.metrics
    assert "drama" in explorer.metrics


def test_get_trajectories(explorer):
    """Test that the TrajectoryExplorer can generate trajectories."""
    trajectories = explorer.get_trajectories(max_length=3)
    assert len(trajectories) > 0
    
    # Check that all trajectories are valid
    for trajectory in trajectories:
        assert isinstance(trajectory, Trajectory)
        assert len(trajectory.intentions) <= 3
        
        # Check that the first intention is a root intention
        first_intention_id = trajectory.intentions[0]["id"]
        assert first_intention_id in explorer.idg.get_root_intentions()


def test_get_trajectories_with_start_intentions(explorer):
    """Test that the TrajectoryExplorer can generate trajectories from specific start intentions."""
    start_intentions = ["visit_grandmother"]
    trajectories = explorer.get_trajectories(max_length=3, start_intentions=start_intentions)
    assert len(trajectories) > 0
    
    # Check that all trajectories start with the specified intention
    for trajectory in trajectories:
        assert trajectory.intentions[0]["id"] == "visit_grandmother"


def test_rank_trajectories_novelty(explorer):
    """Test that the TrajectoryExplorer can rank trajectories by novelty."""
    trajectories = explorer.get_trajectories(max_length=3)
    ranked_trajectories = explorer.rank_trajectories(trajectories, metric="novelty")
    
    # Check that the trajectories are ranked
    assert len(ranked_trajectories) == len(trajectories)
    
    # Check that the ranking is correct
    if len(ranked_trajectories) >= 2:
        first_score = NoveltyMetric().score(ranked_trajectories[0])
        second_score = NoveltyMetric().score(ranked_trajectories[1])
        assert first_score >= second_score


def test_rank_trajectories_coherence(explorer):
    """Test that the TrajectoryExplorer can rank trajectories by coherence."""
    trajectories = explorer.get_trajectories(max_length=3)
    ranked_trajectories = explorer.rank_trajectories(trajectories, metric="coherence")
    
    # Check that the trajectories are ranked
    assert len(ranked_trajectories) == len(trajectories)
    
    # Check that the ranking is correct
    if len(ranked_trajectories) >= 2:
        first_score = CoherenceMetric().score(ranked_trajectories[0])
        second_score = CoherenceMetric().score(ranked_trajectories[1])
        assert first_score >= second_score


def test_rank_trajectories_drama(explorer):
    """Test that the TrajectoryExplorer can rank trajectories by drama."""
    trajectories = explorer.get_trajectories(max_length=3)
    ranked_trajectories = explorer.rank_trajectories(trajectories, metric="drama")
    
    # Check that the trajectories are ranked
    assert len(ranked_trajectories) == len(trajectories)
    
    # Check that the ranking is correct
    if len(ranked_trajectories) >= 2:
        first_score = DramaMetric().score(ranked_trajectories[0])
        second_score = DramaMetric().score(ranked_trajectories[1])
        assert first_score >= second_score


def test_rank_trajectories_custom_metric(explorer):
    """Test that the TrajectoryExplorer can rank trajectories by a custom metric."""
    class CustomMetric:
        def score(self, trajectory):
            return len(trajectory.intentions)
    
    trajectories = explorer.get_trajectories(max_length=3)
    ranked_trajectories = explorer.rank_trajectories(trajectories, metric=CustomMetric())
    
    # Check that the trajectories are ranked
    assert len(ranked_trajectories) == len(trajectories)
    
    # Check that the ranking is correct
    if len(ranked_trajectories) >= 2:
        assert len(ranked_trajectories[0].intentions) >= len(ranked_trajectories[1].intentions)


def test_add_metric(explorer):
    """Test that the TrajectoryExplorer can add a custom metric."""
    class CustomMetric:
        def score(self, trajectory):
            return len(trajectory.intentions)
    
    explorer.add_metric("custom", CustomMetric())
    assert "custom" in explorer.metrics
    
    trajectories = explorer.get_trajectories(max_length=3)
    ranked_trajectories = explorer.rank_trajectories(trajectories, metric="custom")
    
    # Check that the trajectories are ranked
    assert len(ranked_trajectories) == len(trajectories)


def test_get_random_trajectory(explorer):
    """Test that the TrajectoryExplorer can generate a random trajectory."""
    trajectory = explorer.get_random_trajectory(max_length=3)
    assert isinstance(trajectory, Trajectory)
    assert len(trajectory.intentions) <= 3
    
    # Check that the first intention is a root intention
    first_intention_id = trajectory.intentions[0]["id"]
    assert first_intention_id in explorer.idg.get_root_intentions()


def test_get_random_trajectory_with_start_intentions(explorer):
    """Test that the TrajectoryExplorer can generate a random trajectory from specific start intentions."""
    start_intentions = ["visit_grandmother"]
    trajectory = explorer.get_random_trajectory(max_length=3, start_intentions=start_intentions)
    assert isinstance(trajectory, Trajectory)
    assert len(trajectory.intentions) <= 3
    assert trajectory.intentions[0]["id"] == "visit_grandmother"
