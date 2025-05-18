"""
Narrative: A Python library that marries symbolic planning with large language
models (LLMs) to create compelling narratives.

This library provides tools for building Intention Dependency Graphs (IDGs),
exploring narrative trajectories,
and rendering those trajectories into natural language stories using LLMs.
"""

__version__ = "0.2.1"

from narrative.core.idg_builder import IDG, IDGBuilder
from narrative.core.trajectory_explorer import (
    CoherenceMetric,
    DramaMetric,
    NoveltyMetric,
    Trajectory,
    TrajectoryExplorer,
)
from narrative.llm.llm_renderer import LLMAdapter, LLMRenderer, MockLLMAdapter

# Import key classes and functions for easy access
from narrative.schemas.domain import Dependency, Domain, Intention

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
