# Recon v0.2 — Situation Discovery & Actor Resolution

Date: 2026-09-25
Status: Proposed operating boundary

## Purpose

Recon v0.2 extends the validated v0.1 reconstruction instrument from curated case analysis toward continuous discovery of commercially consequential situations.

The question is not:

> Who should we sell to?

The question is:

> **Where is consequential commercial reality changing, and can we reconstruct enough of it to know where human attention belongs?**

## Core loop

```
Situation discovery
      ↓
Organization resolution
      ↓
Actor / role resolution
      ↓
Public evidence / conversation surfaces
      ↓
Observation
      ↓
Situation update
      ↺
```

## Inputs

A situation may enter Recon through:

- public legal or regulatory records;
- public procurement or contract records;
- public company/project material;
- practitioner traces;
- legitimate public conversation surfaces;
- a customer-submitted or manually discovered case.

The source itself is not treated as proof of the underlying claim.

## Situation

A situation is a bounded real-world context in which a commercial commitment, execution event, disagreement, or economic consequence may have changed.

The minimum useful representation is:

- organization(s);
- relevant commercial relationship;
- event or issue;
- time;
- source;
- observation;
- unresolved question;
- known uncertainty.

Do not introduce a general-purpose project/subcase ontology yet.

## Organization resolution

Recon should distinguish:

- the organization named by a source;
- an organization inferred as related;
- the role the organization appears to occupy;
- the evidence supporting the relationship.

Resolution must remain traceable to sources.

## Actor / role resolution

Recon may identify publicly attributable people and roles when they are materially connected to the situation.

It should preserve:

- person identity;
- organization;
- role;
- source;
- observed time;
- relevance to the situation.

It must not infer private attributes, hidden intent, or decision authority without evidence.

## Conversation / evidence surfaces

Recon should identify legitimate public surfaces where the situation can be observed or where relevant practitioner knowledge may exist.

Examples include:

- public professional profiles;
- public company/project pages;
- public legal records;
- public discussions;
- public technical traces.

A surface is an observation channel, not proof.

## Observation

Every material finding becomes an observation with:

- source;
- observed time;
- content/fact;
- relation to the situation;
- uncertainty/evidence stance.

Claims remain separate from observations.

## Update

A situation update records what changed:

- new evidence;
- actor/role resolution;
- changed commercial/economic state;
- new disagreement;
- resolution;
- increased uncertainty.

Recon must preserve previous observations rather than silently rewriting them.

## Human operator boundary

v0.2 remains human-operated for:

- ambiguous identity resolution;
- interpretation of contested claims;
- material economic-state determination;
- deciding whether a situation is commercially consequential;
- initiating engagement.

Automation may assist collection and normalization only where provenance remains visible.

## Explicitly out of scope

- autonomous broad crawling;
- prospect scoring;
- lead ranking;
- automated outreach;
- intent inference;
- prediction;
- private/restricted people-search;
- generic CRM;
- dashboard-first productization;
- giant economic ontology;
- AUM runtime expansion driven only by Recon requirements.

## Success criterion

v0.2 succeeds if, across real situations, the operator can repeatedly move from:

**discovery → reconstructable situation → resolved actors → observable public surface → new observation → updated situation**

without losing provenance or collapsing uncertainty.

The first validation target is operational, not commercial conversion.

## Failure signal

Stop and learn if the same real-world cases repeatedly require:

- facts that cannot be sourced;
- actor resolution that cannot be justified;
- distinctions the representation cannot preserve;
- manual work that adds no epistemic value;
- a new primitive merely to make the workflow convenient.

## Next evidence event

The next meaningful evidence event should be a real commercially consequential situation processed through this loop.

No further synthetic expansion is required before that test.
