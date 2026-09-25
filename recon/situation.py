from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal


ActorRole = Literal["customer", "provider", "decision_maker", "technical", "legal", "arbitrator", "other"]
SurfaceType = Literal["legal_record", "company_page", "professional_profile", "public_discussion", "technical_trace", "procurement_record", "other"]


@dataclass(frozen=True)
class Organization:
    organization_id: str
    name: str
    role: str
    source_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Actor:
    actor_id: str
    name: str
    organization_id: str
    role: str
    source_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ObservationSurface:
    surface_id: str
    surface_type: SurfaceType
    source_id: str
    label: str


@dataclass(frozen=True)
class ResolutionDecision:
    decision_id: str
    subject_type: Literal["organization", "actor", "actor_role", "surface"]
    subject_id: str
    status: Literal["resolved", "ambiguous", "unresolved"]
    basis: str
    source_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class EconomicState:
    object_id: str
    amount: str | None
    currency: str | None
    state: str
    basis: str
    observation_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class SituationUpdate:
    update_id: str
    observed_at: datetime
    description: str
    observation_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class SituationRecord:
    situation_id: str
    title: str
    question: str
    organization_ids: tuple[str, ...] = field(default_factory=tuple)
    actor_ids: tuple[str, ...] = field(default_factory=tuple)
    observation_surface_ids: tuple[str, ...] = field(default_factory=tuple)
    resolution_decisions: tuple[ResolutionDecision, ...] = field(default_factory=tuple)
    observation_ids: tuple[str, ...] = field(default_factory=tuple)
    claim_ids: tuple[str, ...] = field(default_factory=tuple)
    unresolved_questions: tuple[str, ...] = field(default_factory=tuple)
    economic_states: tuple[EconomicState, ...] = field(default_factory=tuple)
    updates: tuple[SituationUpdate, ...] = field(default_factory=tuple)
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.situation_id.strip():
            raise ValueError("situation_id is required")
        if not self.title.strip():
            raise ValueError("title is required")
        if not self.question.strip():
            raise ValueError("question is required")
        if any(not value.strip() for value in self.unresolved_questions):
            raise ValueError("unresolved questions must be non-empty")
