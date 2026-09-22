from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

TrajectoryDirection = Literal["stable", "improving", "deteriorating", "transitioning", "uncertain"]

@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    url: str
    observed_at: datetime
    publisher: str
    statement: str
    entities: tuple[str, ...] = field(default_factory=tuple)
    signal_types: tuple[str, ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class Observation:
    observation_id: str
    source_id: str
    subject_id: str
    observed_at: datetime
    statement: str
    signal_types: tuple[str, ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class State:
    state_id: str
    subject_id: str
    observed_at: datetime
    labels: tuple[str, ...]
    observation_ids: tuple[str, ...]

@dataclass(frozen=True)
class Change:
    change_id: str
    subject_id: str
    from_state_id: str
    to_state_id: str
    detected_at: datetime
    observation_ids: tuple[str, ...]
    added_labels: tuple[str, ...]
    removed_labels: tuple[str, ...]

@dataclass(frozen=True)
class Trajectory:
    trajectory_id: str
    subject_id: str
    direction: TrajectoryDirection
    change_ids: tuple[str, ...]
    observation_ids: tuple[str, ...]
    confidence: float
    rationale: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if not self.change_ids and not self.observation_ids:
            raise ValueError("trajectory requires supporting evidence")
