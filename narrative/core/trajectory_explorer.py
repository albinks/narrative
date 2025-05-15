"""
Trajectory Explorer

This module contains the TrajectoryExplorer class, which generates and ranks trajectories
through an Intention Dependency Graph (IDG).
"""

import random
from typing import Dict, List, Any, Optional, Set, Tuple, Union, Callable, Protocol
from dataclasses import dataclass

from narrative.core.idg_builder import IDG


@dataclass
class Trajectory:
    """
    A trajectory through an IDG.
    
    A trajectory is a sequence of intentions that form a coherent narrative path.
    
    Attributes:
        intentions: A list of intention data dictionaries.
        metadata: Optional additional data associated with the trajectory.
    """
    
    intentions: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None


class MetricProtocol(Protocol):
    """Protocol for trajectory metrics."""
    
    def score(self, trajectory: Trajectory) -> float:
        """Score a trajectory."""
        ...


class NoveltyMetric:
    """
    A metric that scores trajectories based on novelty.
    
    Novelty is measured by the diversity of characters, locations, and intention types.
    """
    
    def score(self, trajectory: Trajectory) -> float:
        """
        Score a trajectory based on novelty.
        
        Args:
            trajectory: The trajectory to score.
            
        Returns:
            A novelty score between 0 and 1.
        """
        if not trajectory.intentions:
            return 0.0
        
        # Count unique characters, locations, and intention IDs
        characters = set()
        locations = set()
        intention_ids = set()
        
        for intention in trajectory.intentions:
            characters.add(intention["character"])
            characters.add(intention["target"])
            locations.add(intention["location"])
            intention_ids.add(intention["id"])
        
        # Calculate diversity scores
        character_diversity = len(characters) / (2 * len(trajectory.intentions))
        location_diversity = len(locations) / len(trajectory.intentions)
        intention_diversity = len(intention_ids) / len(trajectory.intentions)
        
        # Combine scores (equal weighting)
        return (character_diversity + location_diversity + intention_diversity) / 3


class CoherenceMetric:
    """
    A metric that scores trajectories based on coherence.
    
    Coherence is measured by the continuity of characters and locations between adjacent intentions.
    """
    
    def score(self, trajectory: Trajectory) -> float:
        """
        Score a trajectory based on coherence.
        
        Args:
            trajectory: The trajectory to score.
            
        Returns:
            A coherence score between 0 and 1.
        """
        if len(trajectory.intentions) <= 1:
            return 1.0  # A single intention is maximally coherent
        
        continuity_score = 0.0
        
        for i in range(len(trajectory.intentions) - 1):
            current = trajectory.intentions[i]
            next_intention = trajectory.intentions[i + 1]
            
            # Check character continuity
            character_continuity = (
                current["character"] == next_intention["character"] or
                current["character"] == next_intention["target"] or
                current["target"] == next_intention["character"] or
                current["target"] == next_intention["target"]
            )
            
            # Check location continuity
            location_continuity = current["location"] == next_intention["location"]
            
            # Combine continuity scores (equal weighting)
            pair_score = (int(character_continuity) + int(location_continuity)) / 2
            continuity_score += pair_score
        
        return continuity_score / (len(trajectory.intentions) - 1)


class DramaMetric:
    """
    A metric that scores trajectories based on dramatic potential.
    
    Drama is measured by the presence of conflict, character arcs, and emotional intensity.
    """
    
    def score(self, trajectory: Trajectory) -> float:
        """
        Score a trajectory based on dramatic potential.
        
        Args:
            trajectory: The trajectory to score.
            
        Returns:
            A drama score between 0 and 1.
        """
        if not trajectory.intentions:
            return 0.0
        
        # Count conflict indicators
        conflict_count = 0
        character_arcs = set()
        emotional_intensity = 0.0
        
        # Keywords that indicate conflict or emotional intensity
        conflict_keywords = {"eat", "kill", "attack", "fight", "steal", "trick", "deceive"}
        emotional_keywords = {"love", "hate", "fear", "anger", "joy", "sadness", "surprise"}
        
        for intention in trajectory.intentions:
            # Check for conflict in intention ID
            for keyword in conflict_keywords:
                if keyword in intention["id"]:
                    conflict_count += 1
                    break
            
            # Track character arcs (characters that appear in multiple intentions)
            character_arcs.add(intention["character"])
            character_arcs.add(intention["target"])
            
            # Check for emotional intensity in intention ID or description
            for keyword in emotional_keywords:
                if keyword in intention["id"]:
                    emotional_intensity += 1
                    break
                if intention.get("description") and keyword in intention["description"]:
                    emotional_intensity += 0.5
                    break
        
        # Calculate scores
        conflict_score = min(1.0, conflict_count / len(trajectory.intentions))
        character_arc_score = min(1.0, len(character_arcs) / (2 * len(trajectory.intentions)))
        emotional_score = min(1.0, emotional_intensity / len(trajectory.intentions))
        
        # Combine scores (equal weighting)
        return (conflict_score + character_arc_score + emotional_score) / 3


class TrajectoryExplorer:
    """
    Explorer class for generating and ranking trajectories through an IDG.
    """
    
    def __init__(self, idg: IDG):
        """
        Initialize a TrajectoryExplorer with an IDG.
        
        Args:
            idg: The IDG to explore.
        """
        self.idg = idg
        self.metrics = {
            "novelty": NoveltyMetric(),
            "coherence": CoherenceMetric(),
            "drama": DramaMetric(),
        }
    
    def get_trajectories(self, max_length: int = 5, start_intentions: Optional[List[str]] = None) -> List[Trajectory]:
        """
        Generate all possible trajectories through the IDG up to a maximum length.
        
        Args:
            max_length: The maximum length of trajectories to generate.
            start_intentions: Optional list of intention IDs to start trajectories from.
                If not provided, trajectories will start from all root intentions.
                
        Returns:
            A list of trajectories.
        """
        if start_intentions is None:
            start_intentions = list(self.idg.get_root_intentions())
        
        trajectories = []
        
        for start_intention in start_intentions:
            # Start with a trajectory containing just the start intention
            intention_data = self.idg.get_intention_data(start_intention)
            initial_trajectory = Trajectory(intentions=[{"id": start_intention, **intention_data}])
            
            # Use DFS to explore all possible trajectories
            self._explore_trajectories(initial_trajectory, max_length, trajectories)
        
        return trajectories
    
    def _explore_trajectories(self, current_trajectory: Trajectory, max_length: int, 
                             all_trajectories: List[Trajectory]) -> None:
        """
        Recursively explore all possible trajectories from a starting trajectory.
        
        Args:
            current_trajectory: The current trajectory being explored.
            max_length: The maximum length of trajectories to generate.
            all_trajectories: A list to store all generated trajectories.
        """
        # Add the current trajectory to the list
        all_trajectories.append(current_trajectory)
        
        # If we've reached the maximum length, stop exploring
        if len(current_trajectory.intentions) >= max_length:
            return
        
        # Get the last intention in the current trajectory
        last_intention_id = current_trajectory.intentions[-1]["id"]
        
        # Find all intentions that depend on the last intention
        for successor in self.idg.successors(last_intention_id):
            # Create a new trajectory by adding the successor
            successor_data = self.idg.get_intention_data(successor)
            new_intentions = current_trajectory.intentions + [{"id": successor, **successor_data}]
            new_trajectory = Trajectory(intentions=new_intentions)
            
            # Recursively explore from the new trajectory
            self._explore_trajectories(new_trajectory, max_length, all_trajectories)
    
    def rank_trajectories(self, trajectories: List[Trajectory], 
                         metric: Union[str, MetricProtocol] = "novelty") -> List[Trajectory]:
        """
        Rank trajectories according to a metric.
        
        Args:
            trajectories: The trajectories to rank.
            metric: The metric to use for ranking. Can be a string (name of a built-in metric)
                or a custom metric object with a score method.
                
        Returns:
            A list of trajectories sorted by score (highest first).
            
        Raises:
            ValueError: If the metric name is not recognized.
        """
        if isinstance(metric, str):
            if metric not in self.metrics:
                raise ValueError(f"Unknown metric: {metric}")
            metric_obj = self.metrics[metric]
        else:
            metric_obj = metric
        
        # Score and sort trajectories
        scored_trajectories = [(t, metric_obj.score(t)) for t in trajectories]
        scored_trajectories.sort(key=lambda x: x[1], reverse=True)
        
        return [t for t, _ in scored_trajectories]
    
    def add_metric(self, name: str, metric: MetricProtocol) -> None:
        """
        Add a custom metric.
        
        Args:
            name: The name of the metric.
            metric: The metric object.
        """
        self.metrics[name] = metric
    
    def get_random_trajectory(self, max_length: int = 5, 
                             start_intentions: Optional[List[str]] = None) -> Trajectory:
        """
        Generate a random trajectory through the IDG.
        
        Args:
            max_length: The maximum length of the trajectory.
            start_intentions: Optional list of intention IDs to start the trajectory from.
                If not provided, the trajectory will start from a random root intention.
                
        Returns:
            A random trajectory.
        """
        if start_intentions is None:
            start_intentions = list(self.idg.get_root_intentions())
        
        # Choose a random start intention
        start_intention = random.choice(start_intentions)
        intention_data = self.idg.get_intention_data(start_intention)
        trajectory = Trajectory(intentions=[{"id": start_intention, **intention_data}])
        
        # Build the trajectory by randomly choosing successors
        current_intention = start_intention
        while len(trajectory.intentions) < max_length:
            # Get all successors of the current intention
            successors = list(self.idg.successors(current_intention))
            if not successors:
                break  # No more successors, end the trajectory
            
            # Choose a random successor
            next_intention = random.choice(successors)
            next_data = self.idg.get_intention_data(next_intention)
            trajectory.intentions.append({"id": next_intention, **next_data})
            
            current_intention = next_intention
        
        return trajectory
