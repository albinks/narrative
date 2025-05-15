"""
Narrative: A Python library that marries symbolic planning with large language models (LLMs) to create compelling narratives.

This library provides tools for building Intention Dependency Graphs (IDGs), exploring narrative trajectories,
and rendering those trajectories into natural language stories using LLMs.
"""

__version__ = "0.1.0"

# Import key classes and functions for easy access
from narrative.schemas.domain import Domain, Intention, Dependency
from narrative.core.idg_builder import IDGBuilder, IDG
from narrative.core.trajectory_explorer import (
    TrajectoryExplorer,
    Trajectory,
    NoveltyMetric,
    CoherenceMetric,
    DramaMetric,
)
from narrative.llm.llm_renderer import LLMRenderer, LLMAdapter, MockLLMAdapter

# Define what's available for import with `from narrative import *`
__all__ = [
    "Domain",
    "Intention",
    "Dependency",
    "IDGBuilder",
    "IDG",
    "TrajectoryExplorer",
    "Trajectory",
    "NoveltyMetric",
    "CoherenceMetric",
    "DramaMetric",
    "LLMRenderer",
    "LLMAdapter",
    "MockLLMAdapter",
]
