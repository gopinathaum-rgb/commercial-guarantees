from __future__ import annotations
from collections import defaultdict
from datetime import datetime
import json
from pathlib import Path
from .model import Change, Observation, SourceRecord, State, Trajectory

NEGATIVE = {"delay","delayed","dispute","disputed","termination","terminated","escalation","escalated","incident","failure","failed","blocked","blacklisting","arbitration","claim","withheld","critical defects"}
POSITIVE = {"signed off","accepted","acceptance","completed","completion","go-live","production","stabilized","resolved","successful"}
TRANSITION = {"uat","implementation","migration","deployment","go-live","handover","rollout","cutover"}

def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

def load_sources(path: Path) -> list[SourceRecord]:
    records = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        records.append(SourceRecord(raw["source_id"], raw["url"], parse_dt(raw["observed_at"]), raw["publisher"], raw["statement"], tuple(raw.get("entities", [])), tuple(raw.get("signal_types", [])), raw.get("stance", "procedural_fact")))
    return sorted(records, key=lambda x: x.observed_at)

def normalize(records: list[SourceRecord]) -> list[Observation]:
    out = []
    n = 0
    for source in records:
        for subject in source.entities or ("unknown",):
            n += 1
            out.append(Observation(f"obs-{n:04d}", source.source_id, subject, source.observed_at, source.statement, source.signal_types, source.stance))
    return out

def state_for(observation: Observation) -> State:
    labels = set(observation.signal_types)
    text = observation.statement.lower()
    for label in NEGATIVE | POSITIVE | TRANSITION:
        if label in text:
            labels.add(label)
    return State(f"state-{observation.observation_id}", observation.subject_id, observation.observed_at, tuple(sorted(labels)), (observation.observation_id,))

def detect_changes(observations: list[Observation]) -> list[Change]:
    grouped = defaultdict(list)
    for observation in observations:
        grouped[observation.subject_id].append(observation)
    changes = []
    n = 0
    for subject, items in grouped.items():
        items.sort(key=lambda x: x.observed_at)
        previous = None
        for item in items:
            current = state_for(item)
            if previous is not None:
                added = tuple(sorted(set(current.labels) - set(previous.labels)))
                removed = tuple(sorted(set(previous.labels) - set(current.labels)))
                if added or removed:
                    n += 1
                    changes.append(Change(f"chg-{n:04d}", subject, previous.state_id, current.state_id, current.observed_at, current.observation_ids, added, removed))
            previous = current
    return changes

def assess_trajectory(subject_id: str, observations: list[Observation], changes: list[Change]) -> Trajectory:
    subject_obs = [o for o in observations if o.subject_id == subject_id]
    text = " ".join(o.statement.lower() for o in subject_obs)
    negative = sum(1 for t in NEGATIVE if t in text)
    positive = sum(1 for t in POSITIVE if t in text)
    transition = sum(1 for t in TRANSITION if t in text)
    subject_changes = [c for c in changes if c.subject_id == subject_id]
    if negative > positive and negative:
        direction, rationale = "deteriorating", "Observed sources contain more negative-state signals than positive-state signals."
    elif positive > negative and positive:
        direction, rationale = "improving", "Observed sources contain more positive-state signals than negative-state signals."
    elif transition:
        direction, rationale = "transitioning", "Observed sources indicate an active implementation or delivery transition without enough evidence to call the direction positive or negative."
    else:
        direction, rationale = "uncertain", "Available observations do not support a directional assessment."
    confidence = min(0.9, 0.4 + 0.15 * max(0, len(subject_obs) - 1) + 0.1 * min(len(subject_changes), 3))
    return Trajectory(f"traj-{subject_id.lower().replace(' ', '-')}", subject_id, direction, tuple(c.change_id for c in subject_changes), tuple(o.observation_id for o in subject_obs), round(confidence, 2), rationale)

def render_report(records, observations, changes, trajectory) -> str:
    sources = {r.source_id: r for r in records}
    lines = [f"SITUATION — {trajectory.subject_id}", "", f"Trajectory: {trajectory.direction.upper()} (confidence {trajectory.confidence:.2f})", f"Rationale: {trajectory.rationale}", "", "Observed changes:"]
    subject_changes = [c for c in changes if c.subject_id == trajectory.subject_id]
    lines += [f"- {c.detected_at.isoformat()}: +{', '.join(c.added_labels) or 'none'} / -{', '.join(c.removed_labels) or 'none'}" for c in subject_changes] or ["- None detected from the supplied records"]
    lines += ["", "Evidence:"]
    for o in observations:
        if o.subject_id == trajectory.subject_id:
            s = sources[o.source_id]
            lines.append(f"- {o.observed_at.date()} | {o.stance.upper()} | {s.publisher} | {o.statement} | {s.url}")
    lines += ["", "Uncertainty:", "- This report reflects source statements and normalized signals; it does not independently authenticate the underlying claims.", "- Repeated reporting is not treated as independent verification.", "- Trajectory is an observed-direction assessment, not a prediction."]
    return "\n".join(lines) + "\n"
