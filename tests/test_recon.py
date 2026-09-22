from pathlib import Path
from recon.engine import assess_trajectory, detect_changes, load_sources, normalize

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
