from datetime import datetime, timezone

import pytest

from recon.situation import (
    Actor,
    EconomicState,
    ObservationSurface,
    Organization,
    SituationRecord,
    SituationUpdate,
)


def test_situation_record_is_thin_context_layer():
    record = SituationRecord(
        situation_id="WAPCOS-CYFUTURE",
        title="WAPCOS × CYFUTURE ERP dispute",
        question="What implementation and economic consequences can actually be established?",
        organization_ids=("wapcos", "cyfuture"),
        actor_ids=("arun-arora", "himanshu-jangid"),
        observation_surface_ids=("court-22-may", "practitioner-profile"),
        observation_ids=("obs-0001", "obs-0002"),
        claim_ids=("claim-001",),
        unresolved_questions=("Which contractual milestones were satisfied?",),
        economic_states=(
            EconomicState(
                object_id="wapcos-claim",
                amount="200000000",
                currency="INR",
                state="claimed",
                basis="party assertion recorded by court",
                observation_ids=("obs-0006",),
            ),
        ),
        updates=(
            SituationUpdate(
                update_id="update-001",
                observed_at=datetime(2026, 5, 22, tzinfo=timezone.utc),
                description="Court referred merits to arbitration while recording competing positions.",
                observation_ids=("obs-0007",),
            ),
        ),
        created_at=datetime(2026, 4, 22, tzinfo=timezone.utc),
    )

    assert record.situation_id == "WAPCOS-CYFUTURE"
    assert record.organization_ids == ("wapcos", "cyfuture")
    assert record.economic_states[0].state == "claimed"
    assert record.updates[0].observation_ids == ("obs-0007",)


def test_organization_actor_and_surface_retain_source_traceability():
    org = Organization("wapcos", "WAPCOS Limited", "customer", ("source-001",))
    actor = Actor("arun-arora", "Arun Arora", "wapcos", "GM, IT", ("source-001",))
    surface = ObservationSurface(
        "court-22-may",
        "legal_record",
        "source-001",
        "Delhi High Court order dated 22 May 2026",
    )

    assert org.source_ids == ("source-001",)
    assert actor.organization_id == org.organization_id
    assert actor.source_ids == ("source-001",)
    assert surface.source_id == "source-001"


def test_unresolved_questions_cannot_be_empty_strings():
    with pytest.raises(ValueError, match="unresolved questions"):
        SituationRecord(
            situation_id="s1",
            title="Situation",
            question="Question",
            unresolved_questions=("",),
        )
