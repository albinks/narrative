"""
Domain Schema

This module defines the schema for the domain model, which is the foundation of the NarrativeIDG library.
A domain consists of characters, locations, intentions, and dependencies between intentions.
"""
# flake8: noqa: E501

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, validator


class Intention(BaseModel):
    """
    An intention represents a character's goal or desire.

    Attributes:
        id: A unique identifier for the intention.
        character: The character who has this intention.
        target: The target of the intention (usually another character).
        location: The location where the intention takes place.
        description: An optional description of the intention.
        metadata: Optional additional data associated with the intention.
    """

    id: str
    character: str
    target: str
    location: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Dependency(BaseModel):
    """
    A dependency represents a relationship between two intentions.

    Attributes:
        from_intention: The intention that depends on another.
        to_intention: The intention that is depended upon.
        type: The type of dependency (intentional or motivational).
        description: An optional description of the dependency.
        metadata: Optional additional data associated with the dependency.
    """

    from_intention: str
    to_intention: str
    type: Literal["intentional", "motivational"]
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Domain(BaseModel):
    """
    A domain represents a narrative world with characters, locations, intentions, and dependencies.

    Attributes:
        characters: A list of character names.
        locations: A list of location names.
        intentions: A list of intentions in the domain.
        dependencies: A list of dependencies between intentions.
        name: An optional name for the domain.
        description: An optional description of the domain.
        metadata: Optional additional data associated with the domain.
    """

    characters: List[str]
    locations: List[str]
    intentions: List[Union[Intention, Dict[str, Any]]]
    dependencies: List[Union[Dependency, Dict[str, Any]]]
    name: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    @validator("intentions", pre=True, each_item=True)
    def validate_intentions(cls, v: Any) -> Union[Intention, Any]:
        """Validate and convert intentions to Intention objects."""
        if isinstance(v, dict):
            return Intention(**v)
        return v

    @validator("dependencies", pre=True, each_item=True)
    def validate_dependencies(cls, v: Any) -> Union[Dependency, Any]:
        """Validate and convert dependencies to Dependency objects."""
        if isinstance(v, dict):
            return Dependency(**v)
        return v

    class Config:
        """Configuration for the Domain model."""

        arbitrary_types_allowed = True
        json_encoders = {
            Intention: lambda v: v.model_dump(),
            Dependency: lambda v: v.model_dump(),
        }
