from datetime import datetime, timezone

import pytest

from pathlib import Path

from recon.engine import build_situation_record, load_sources, normalize
from recon.model import Claim
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


def test_wapcos_sources_load_into_situation_without_duplicate_evidence():
    records = load_sources(Path("recon/sources/wapcos_cyfuture.jsonl"))
    observations = normalize(records)
    claim = Claim(
        claim_id="claim-wapcos-performance",
        subject_id="WAPCOS-CYFUTURE",
        statement="WAPCOS alleged stipulated implementation terms and timelines were not fulfilled.",
        claim_type="performance_claim",
        stance="party_allegation",
        status="disputed",
        observation_ids=("obs-0004",),
    )
    record = build_situation_record(
        "WAPCOS-CYFUTURE",
        "WAPCOS × CYFUTURE ERP dispute",
        "What implementation and economic consequences can actually be established?",
        records,
        observations,
        organizations=(
            Organization("wapcos", "WAPCOS Limited", "customer", ("wapcos-001",)),
            Organization("cyfuture", "CYFUTURE India Private Limited", "provider", ("wapcos-002",)),
        ),
        actors=(
            Actor("arun-arora", "Arun Arora", "wapcos", "GM, IT", ("wapcos-006",)),
        ),
        observation_surfaces=(
            ObservationSurface("court-22-may", "legal_record", "wapcos-001", "Delhi High Court record"),
            ObservationSurface("practitioner-trace", "professional_profile", "wapcos-003", "Practitioner trace"),
        ),
        claims=(claim,),
        unresolved_questions=("Which contractual milestones were satisfied?",),
    )
    assert len(record.observation_ids) == len(observations) == 7
    assert record.claim_ids == ("claim-wapcos-performance",)
    assert record.organization_ids == ("wapcos", "cyfuture")
    assert record.actor_ids == ("arun-arora",)
    assert record.observation_surface_ids == ("court-22-may", "practitioner-trace")
    assert record.observation_ids[0] == "obs-0001"


CASE_EXPECTATIONS = {
    "sage_baidyanath.jsonl": ("SAGE-BAIDYANATH", "successful Go-Live was not established"),
    "ntro_corporate_infotech.jsonl": ("NTRO-CORPORATE-INFOTECH", "OSAT completion was deemed"),
    "velocis_concor.jsonl": ("VELOCIS-CONCOR", "performance bank guarantee"),
    "videocon_ibm.jsonl": ("VIDEOCON-IBM", "project-by-project"),
}


@pytest.mark.parametrize("filename", CASE_EXPECTATIONS)
def test_four_real_cases_fit_same_situation_boundary(filename):
    subject, expected_phrase = CASE_EXPECTATIONS[filename]
    records = load_sources(Path("recon/sources") / filename)
    observations = normalize(records)

    organizations = (
        Organization(f"{subject.lower()}-customer", "Customer", "customer", (records[0].source_id,)),
        Organization(f"{subject.lower()}-provider", "Provider", "provider", (records[0].source_id,)),
    )
    surfaces = tuple(
        ObservationSurface(
            f"{subject.lower()}-surface-{i}",
            "legal_record",
            record.source_id,
            record.publisher,
        )
        for i, record in enumerate(records, 1)
    )
    record = build_situation_record(
        subject,
        subject,
        "What completion, performance, and economic consequences can actually be established?",
        records,
        observations,
        organizations=organizations,
        observation_surfaces=surfaces,
        unresolved_questions=("Which contractual condition controls the relevant economic consequence?",),
    )

    assert record.situation_id == subject
    assert len(record.observation_ids) == len(observations)
    assert len(record.observation_surface_ids) == len(records)
    assert record.unresolved_questions
    assert all(observation_id in record.observation_ids for observation_id in record.observation_ids)
    assert expected_phrase.lower() in " ".join(o.statement.lower() for o in observations)
