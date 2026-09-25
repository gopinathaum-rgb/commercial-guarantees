# Recon v0.2 — Context Resolution Protocol

Date: 2026-09-25

## Purpose

After a consequential situation is discovered, Recon must establish enough real-world context to answer:

- which organizations are involved;
- what relationship each organization has to the situation;
- which people/roles are actually evidenced;
- which public evidence or conversation surfaces are relevant;
- what remains unresolved.

This is **context resolution**, not prospecting.

## Operating rule

> Never promote an inferred identity into a resolved actor.

Recon may preserve a candidate, hypothesis, or unresolved question, but a resolved organization, actor, role, or surface must point to source evidence.

## Resolution sequence

### 1. Situation anchor

Start from a consequential situation already supported by one or more source records.

Required:
- situation identity;
- bounded question;
- at least one source.

Do not begin with a person or company list.

### 2. Organization resolution

For each organization attached to the situation, record:

- stable organization identifier;
- observed name;
- relationship/role in the situation;
- source IDs supporting the association.

Examples of roles:
- customer;
- provider;
- counterparty;
- regulator;
- adjudicator.

The role is contextual. It does not imply fault, entitlement, or legal status.

### 3. Actor/role resolution

Add a person only when a source connects that person to the situation.

Record:
- actor identifier;
- observed name;
- organization;
- role as evidenced;
- supporting source IDs.

A professional profile can establish that a person describes work associated with a situation. It does not by itself establish contractual authority, decision rights, or responsibility.

If the identity or role cannot be established, keep the person out of the resolved actor set and preserve the unresolved question.

### 4. Observation-surface resolution

A surface is a public place from which evidence can be observed.

Examples:
- legal record;
- procurement record;
- company page;
- professional profile;
- public discussion;
- technical trace.

A surface is not a lead score and not a contact record.

Record:
- surface identifier;
- surface type;
- source ID;
- human-readable label.

### 5. Cross-check

Before context is attached to a SituationRecord:

- every organization must cite known source IDs;
- every actor must cite known source IDs and a known organization;
- every surface must cite a known source ID;
- no actor is promoted from name similarity alone;
- no role is inferred from title alone when the source does not connect the person to the situation;
- disputed source material remains disputed.

### 6. Human resolution gate

The v0.2 operator decides whether an identity/role association is:

- resolved enough to record;
- ambiguous and therefore not promoted;
- unresolved and retained as a question.

The system validates references; it does not manufacture identity certainty.

## What v0.2 deliberately does not do

- autonomous web crawling;
- unrestricted people search;
- prospect scoring;
- contact enrichment;
- intent inference;
- responsibility inference;
- automated outreach;
- probabilistic identity matching;
- automatic contradiction resolution.

## Five-case acceptance test

The protocol must work across:

- WAPCOS × CYFUTURE;
- Sage Technologies × Shree Baidyanath;
- NTRO × Corporate Infotech;
- Velocis × CONCOR;
- Videocon Telecommunications × IBM India.

A case passes when Recon can move from source-backed situation → organizations → evidenced actors/roles where available → observation surfaces, while leaving unsupported identities unresolved.

## Current implementation boundary

The existing SituationRecord and build_situation_record() provide the validation boundary.

The next implementation question is narrower:

> Can Recon capture an operator's resolution decision without turning that decision into an unsupported fact?

Until that question is answered with real cases, do not add automated identity resolution or a new identity ontology.
