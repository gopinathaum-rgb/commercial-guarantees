# GitHub channel: customer discovery operations

## Purpose

Use public GitHub issue discussions as a second discovery channel alongside email. The aim is to find real, current ERP implementation situations and earn trust by contributing useful analysis—not to turn issue trackers into cold-outreach lists.

## What the channel can establish

- Public evidence that practitioners encounter implementation, migration, deployment, acceptance, cutover, integration, or handover problems.
- The vocabulary practitioners use to describe those problems.
- Whether a source thread contains an unresolved question where a careful, evidence-based contribution would help.
- Whether an author independently asks for assistance or a relevant service.

It cannot establish that an author controls a budget, has authority, wants to buy, or is a qualified prospect.

## Automated workflow

The scheduled GitHub Action searches open, recently updated issues in:
- `frappe/erpnext`
- `frappe/frappe`
- `odoo/odoo`

It filters for implementation-lifecycle language and appends only previously unseen source links and short, email-redacted excerpts to one durable issue: **GitHub channel — customer discovery queue**.

Schedule: weekdays, 08:00 Asia/Kolkata (02:30 UTC), plus manual dispatch.

## Human operating protocol

For each new source:
1. Read the complete issue and comments; do not rely on the excerpt.
2. Classify it as (a) implementation lifecycle problem, (b) isolated product defect, (c) feature request, or (d) insufficient evidence.
3. Identify the precise question the author needs answered.
4. Draft a technically useful answer that stands on its own.
5. Publish only when the answer is accurate, relevant, and genuinely helpful to the public thread.
6. Do not add promotional links, solicit private records, or pitch the audit unless the author explicitly invites service recommendations or asks for help.
7. If an author independently expresses interest, move the interaction to a private, consent-based channel and qualify the real situation, decision owner, authority, deadline, evidence access, and willingness to pay.

## Commercial evidence ladder

| Signal | What it means | Count as buyer? |
|---|---|---:|
| Issue found | Publicly described problem context | No |
| Useful answer published | Contribution and visibility | No |
| Author replies or asks a follow-up | Engagement | No |
| Author asks about the audit/service | Inbound service interest | Not yet |
| Current consequential situation + decision owner identified | Potentially qualified opportunity | Not yet |
| Scope and fee accepted in writing | Commercial acceptance | Yes, accepted engagement |
| Advance payment independently evidenced | Paid engagement started | Yes, first customer rupee |

## Safety and integrity boundaries

- No automated comments on third-party repositories.
- No mass mentions, unsolicited DMs, scraping of private data, or inferred buying-intent scores.
- No claims that a public issue is a customer, lead, loss, dispute, or active buying process without direct evidence.
- Never ask people to post contracts, customer data, credentials, or sensitive records publicly.
- Keep all public answers useful even if no commercial conversation follows.
- Pricing, contractual scope, sensitive disclosures, and acceptance of an engagement remain owner decisions.

## Success measure

The channel succeeds only when it contributes to a real, consent-based commercial conversation and ultimately a paid engagement. Repository activity, stars, comments, issue volume, and traffic are not revenue.
