from pathlib import Path

from recon.engine import (
    assess_trajectory,
    detect_changes,
    load_sources,
    normalize,
    render_report,
)
from recon.model import Claim, EvidenceLink


def test_demo_records_produce_changes_and_deteriorating_trajectory():
    records = load_sources(Path("recon/sources/demo.jsonl"))
    observations = normalize(records)
    changes = detect_changes(observations)
    trajectory = assess_trajectory("DemoCo", observations, changes)
    assert len(observations) == 3
    assert len(changes) == 2
    assert trajectory.direction == "deteriorating"
    assert trajectory.change_ids


def test_trajectory_requires_evidence():
    records = load_sources(Path("recon/sources/demo.jsonl"))
    observations = normalize(records)
    changes = detect_changes(observations)
    trajectory = assess_trajectory("DemoCo", observations, changes)
    assert trajectory.observation_ids
    assert "prediction" not in trajectory.rationale.lower()


def test_wapcos_cyfuture_replay_preserves_manual_investigation_boundary():
    records = load_sources(Path("recon/sources/wapcos_cyfuture.jsonl"))
    observations = normalize(records)
    changes = detect_changes(observations)
    trajectory = assess_trajectory("WAPCOS-CYFUTURE", observations, changes)
    report = render_report(records, observations, changes, trajectory)
    assert len(records) == 7
    assert len(observations) == 7
    assert trajectory.direction == "deteriorating"
    assert len(trajectory.change_ids) >= 1
    assert "2026-04-16" in report
    assert "2026-04-17" in report
    assert "2026-04-22" in report
    assert "2026-05-22" in report
    assert "arbitration" in report.lower()
    assert "PARTY_ALLEGATION" in report
    assert "COURT_DIRECTION" in report
    assert "COURT_RESERVATION" in report
    assert "not a prediction" in report.lower()
    assert "does not independently authenticate" in report
    assert trajectory.confidence == 0.55
    assert "contested" in trajectory.rationale.lower()


def test_wapcos_replay_retains_source_traceability():
    records = load_sources(Path("recon/sources/wapcos_cyfuture.jsonl"))
    observations = normalize(records)
    changes = detect_changes(observations)
    trajectory = assess_trajectory("WAPCOS-CYFUTURE", observations, changes)
    report = render_report(records, observations, changes, trajectory)
    observation_sources = {o.source_id for o in observations}
    for record in records:
        assert record.source_id in observation_sources
        assert record.url in report
    assert "merits open" in records[-1].statement.lower()


def test_wapcos_replay_preserves_evidence_stance():
    records = load_sources(Path("recon/sources/wapcos_cyfuture.jsonl"))
    observations = normalize(records)
    assert [o.stance for o in observations] == [r.stance for r in records]
    assert observations[3].stance == "party_allegation"
    assert observations[5].stance == "court_direction"
    assert observations[6].stance == "court_reservation"


def test_claim_requires_explicit_evidence():
    records = load_sources(Path("recon/sources/wapcos_cyfuture.jsonl"))
    observations = normalize(records)
    claim = Claim(
        claim_id="claim-wapcos-001",
        subject_id="WAPCOS-CYFUTURE",
        statement="CYFUTURE failed to fulfil stipulated implementation obligations.",
        claim_type="performance_claim",
        stance="party_allegation",
        status="disputed",
        observation_ids=(observations[3].observation_id,),
    )
    link = EvidenceLink(
        claim_id=claim.claim_id,
        observation_id=observations[3].observation_id,
        relation="supports",
    )
    assert link.claim_id == claim.claim_id
    assert link.observation_id == observations[3].observation_id
    assert link.relation == "supports"


def test_sage_replay_can_represent_contract_condition_and_adjudication():
    records = load_sources(Path("recon/sources/sage_baidyanath.jsonl"))
    observations = normalize(records)

    success_claim = Claim(
        claim_id="claim-sage-go-live",
        subject_id="SAGE-BAIDYANATH",
        statement="Successful Go-Live was achieved.",
        claim_type="contractual_condition",
        stance="party_allegation",
        status="disputed",
        observation_ids=(observations[1].observation_id, observations[2].observation_id),
    )
    success_links = (
        EvidenceLink(success_claim.claim_id, observations[1].observation_id, "supports"),
        EvidenceLink(success_claim.claim_id, observations[2].observation_id, "contradicts"),
    )

    finding = Claim(
        claim_id="finding-sage-go-live",
        subject_id="SAGE-BAIDYANATH",
        statement="Successful Go-Live was not established.",
        claim_type="adjudicated_finding",
        stance="procedural_fact",
        status="adjudicated",
        observation_ids=(observations[3].observation_id,),
    )
    finding_link = EvidenceLink(
        finding.claim_id,
        observations[3].observation_id,
        "resolves",
    )

    assert success_claim.status == "disputed"
    assert {link.relation for link in success_links} == {"supports", "contradicts"}
    assert finding.status == "adjudicated"
    assert finding_link.relation == "resolves"

def test_claim_evidence_relationships_render_in_report():
    records = load_sources(Path("recon/sources/sage_baidyanath.jsonl"))
    observations = normalize(records)
    changes = detect_changes(observations)
    trajectory = assess_trajectory("SAGE-BAIDYANATH", observations, changes)
    claim = Claim("claim-sage-go-live", "SAGE-BAIDYANATH", "Successful Go-Live was achieved.", "contractual_condition", "party_allegation", "disputed", (observations[1].observation_id, observations[2].observation_id))
    links = (
        EvidenceLink(claim.claim_id, observations[1].observation_id, "supports"),
        EvidenceLink(claim.claim_id, observations[2].observation_id, "contradicts"),
    )
    report = render_report(records, observations, changes, trajectory, (claim,), links)
    assert "CLAIMS:" in report
    assert "claim-sage-go-live" in report
    assert "supports obs-0002" in report
    assert "contradicts obs-0003" in report
    assert "Claim status is operator-supplied" in report



def test_ntro_replay_can_represent_waiver_and_adjudicated_completion():
    records = load_sources(Path("recon/sources/ntro_corporate_infotech.jsonl"))
    observations = normalize(records)
    changes = detect_changes(observations)
    trajectory = assess_trajectory("NTRO-CORPORATE-INFOTECH", observations, changes)

    condition = Claim(
        "claim-ntro-osat-condition",
        "NTRO-CORPORATE-INFOTECH",
        "Successful OSAT is a contractual condition for the relevant payment, warranty, and PBG consequences.",
        "contractual_condition",
        "procedural_fact",
        "asserted",
        (observations[0].observation_id,),
    )
    dispute = Claim(
        "claim-ntro-osat-disputed",
        "NTRO-CORPORATE-INFOTECH",
        "OSAT remained incomplete and the balance payment was not due.",
        "performance_claim",
        "party_allegation",
        "disputed",
        (observations[2].observation_id,),
    )
    finding = Claim(
        "finding-ntro-osat-complete",
        "NTRO-CORPORATE-INFOTECH",
        "OSAT was deemed completed on 17 March 2020 for contractual consequences.",
        "adjudicated_finding",
        "procedural_fact",
        "adjudicated",
        (observations[1].observation_id, observations[4].observation_id),
    )

    links = (
        EvidenceLink(condition.claim_id, observations[0].observation_id, "supports"),
        EvidenceLink(dispute.claim_id, observations[2].observation_id, "supports"),
        EvidenceLink(finding.claim_id, observations[1].observation_id, "supports"),
        EvidenceLink(finding.claim_id, observations[4].observation_id, "resolves"),
    )

    report = render_report(
        records,
        observations,
        changes,
        trajectory,
        (condition, dispute, finding),
        links,
    )

    assert len(records) == 5
    assert trajectory.observation_ids
    assert condition.status == "asserted"
    assert dispute.status == "disputed"
    assert finding.status == "adjudicated"
    assert "claim-ntro-osat-disputed" in report
    assert "resolves obs-0005" in report
    assert "deemed OSAT completed" in report


def test_velocis_concor_replay_can_represent_guarantee_consequence_without_merits_finality():
    records = load_sources(Path("recon/sources/velocis_concor.jsonl"))
    observations = normalize(records)
    changes = detect_changes(observations)
    trajectory = assess_trajectory("VELOCIS-CONCOR", observations, changes)

    condition = Claim(
        "claim-velocis-milestones",
        "VELOCIS-CONCOR",
        "Software acceptance and the preceding implementation/testing milestones were contractual conditions in the project schedule.",
        "contractual_condition",
        "procedural_fact",
        "asserted",
        (observations[0].observation_id,),
    )
    vendor_claim = Claim(
        "claim-velocis-signoff",
        "VELOCIS-CONCOR",
        "The vendor had completed the relevant milestones and CONCOR had not provided sign-off.",
        "performance_claim",
        "party_allegation",
        "disputed",
        (observations[1].observation_id,),
    )
    respondent_claim = Claim(
        "claim-velocis-delay",
        "VELOCIS-CONCOR",
        "Milestones 5 to 10 remained incomplete by 31 March 2024.",
        "counter_claim",
        "party_response",
        "disputed",
        (observations[2].observation_id,),
    )
    procedural = Claim(
        "finding-velocis-bguarantee",
        "VELOCIS-CONCOR",
        "The Court did not stay termination and did not find grounds to restrain performance-bank-guarantee invocation on the supplied record.",
        "procedural_claim",
        "procedural_fact",
        "adjudicated",
        (observations[3].observation_id, observations[5].observation_id),
    )

    links = (
        EvidenceLink(condition.claim_id, observations[0].observation_id, "supports"),
        EvidenceLink(vendor_claim.claim_id, observations[1].observation_id, "supports"),
        EvidenceLink(respondent_claim.claim_id, observations[2].observation_id, "supports"),
        EvidenceLink(procedural.claim_id, observations[3].observation_id, "supports"),
        EvidenceLink(procedural.claim_id, observations[5].observation_id, "resolves"),
    )

    report = render_report(
        records,
        observations,
        changes,
        trajectory,
        (condition, vendor_claim, respondent_claim, procedural),
        links,
    )

    assert len(records) == 6
    assert len(observations) == 6
    assert trajectory.direction == "deteriorating"
    assert trajectory.confidence == 0.55
    assert "performance guarantee" in report.lower()
    assert "resolves obs-0006" in report
    assert "not a prediction" in report.lower()
    assert "does not independently authenticate" in report
