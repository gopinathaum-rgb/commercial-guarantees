from pathlib import Path
from recon.engine import assess_trajectory, detect_changes, load_sources, normalize, render_report

def test_demo_records_produce_changes_and_deteriorating_trajectory():
    records=load_sources(Path("recon/sources/demo.jsonl")); observations=normalize(records); changes=detect_changes(observations); trajectory=assess_trajectory("DemoCo",observations,changes)
    assert len(observations)==3
    assert len(changes)==2
    assert trajectory.direction=="deteriorating"
    assert trajectory.change_ids

def test_trajectory_requires_evidence():
    records=load_sources(Path("recon/sources/demo.jsonl")); observations=normalize(records); changes=detect_changes(observations); trajectory=assess_trajectory("DemoCo",observations,changes)
    assert trajectory.observation_ids
    assert "prediction" not in trajectory.rationale.lower()

def test_wapcos_cyfuture_replay_preserves_manual_investigation_boundary():
    records=load_sources(Path("recon/sources/wapcos_cyfuture.jsonl"))
    observations=normalize(records)
    changes=detect_changes(observations)
    trajectory=assess_trajectory("WAPCOS-CYFUTURE",observations,changes)
    report=render_report(records,observations,changes,trajectory)
    assert len(records)==7
    assert len(observations)==7
    assert trajectory.direction=="deteriorating"
    assert len(trajectory.change_ids)>=1
    assert "2026-04-16" in report
    assert "2026-04-17" in report
    assert "2026-04-22" in report
    assert "2026-05-22" in report
    assert "arbitration" in report.lower()
    assert "not a prediction" in report.lower()
    assert "does not independently authenticate" in report.lower()

def test_wapcos_replay_retains_source_traceability():
    records=load_sources(Path("recon/sources/wapcos_cyfuture.jsonl"))
    observations=normalize(records)
    changes=detect_changes(observations)
    trajectory=assess_trajectory("WAPCOS-CYFUTURE",observations,changes)
    report=render_report(records,observations,changes,trajectory)
    observation_sources={o.source_id for o in observations}
    for record in records:
        assert record.source_id in observation_sources
        assert record.url in report
    assert "merits open" in records[-1].statement.lower()
