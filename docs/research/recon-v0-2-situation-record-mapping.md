# Recon v0.2 — SituationRecord Mapping

Date: 2026-09-25

## Decision

SituationRecord is a thin context layer around the validated Recon v0.1 evidence chain.

Existing v0.1 primitives remain authoritative for evidence reconstruction:

source → observation → claim → evidence link → state/change → trajectory

SituationRecord adds the real-world context that v0.1 leaves implicit:

situation → organizations → actors/roles → observation surfaces → economic snapshot → updates

## Mapping

| SituationRecord | Existing primitive | Decision |
|---|---|---|
| situation identity | subject_id / report context | Add explicit situation_id |
| organizations | SourceRecord.entities | Add explicit organization context |
| actors/roles | none in v0.1 | Add minimal actor context with source IDs |
| observation surfaces | SourceRecord | Add explicit reusable surface context |
| observations | Observation | Reference existing observation IDs |
| claims | Claim | Reference existing claim IDs |
| disagreements | Claim + EvidenceLink | Do not create a second disagreement model yet |
| economic state | Claim/reasoning | Add minimal snapshot only; no ontology |
| unresolved questions | operator reasoning | Add explicit strings; preserve uncertainty |
| updates | Change + Observation | Add situation-level update references |
| traceability | source_id / observation_id | Preserve IDs; no duplicated evidence objects |

## Explicit non-decisions

We are not introducing:
- a second evidence model;
- a second claim model;
- a project/subcase ontology;
- autonomous identity resolution;
- economic adjudication;
- prospect scoring;
- crawler infrastructure;
- AUM runtime changes.

## Why this boundary

The WAPCOS × CYFUTURE situation required context that was not naturally represented by subject-level observations alone. But its evidence could already be represented by the v0.1 chain.

Therefore the correct v0.2 move is to add context, not replace the epistemic core.

## Acceptance test

A SituationRecord must be able to point to existing observation and claim IDs and preserve:
- where the information came from;
- who/which organization it concerns;
- what role an actor appears to hold;
- which public surface produced the observation;
- what economic state is being asserted;
- what changed;
- what remains unresolved.

The SituationRecord itself does not authenticate claims.

## Next implementation boundary

The next step is to connect the SituationRecord to the existing Recon engine so a real source set can be loaded into a situation without duplicating observations or claims.

Only after that integration works should broader discovery/actor-resolution automation be considered.
