# GitHub channel: customer discovery operations

## Purpose
Use public ERP implementation discussions to find situations where evidence reconstruction may help a real commercial decision. This is one acquisition channel alongside written email outreach. It is not a buyer detector.

## Automated discovery
The weekday GitHub Action searches recently updated open issues in Frappe, ERPNext and Odoo. It searches implementation, migration, deployment and acceptance topics; reads bounded pages of issue comments; classifies text using lifecycle, context and explicit decision-language signals; redacts email addresses and common credential-like strings; and deduplicates against paginated queue history.

Decision-language matches (acceptance tests, sign-off, milestone payment, invoice, holdback, scope dispute, production approval) are reading priorities only. They do not establish a contract, dispute, budget, buyer intent, authority or willingness to pay.

## Reviewer protocol
1. Read the full issue and discussion, including latest updates.
2. Separate direct statements, reported claims, inference and unknowns.
3. Identify the actual milestone, obligation, acceptance/payment decision and accountable owner only when supported by source evidence.
4. Determine whether an evidence-reconstruction contribution would genuinely help.
5. Draft a technically substantive response that stands alone.
6. Do not publish to third-party repositories automatically. Public posting under the owner's identity requires approval.
7. If the author independently asks about relevant services, continue privately only with consent; qualify current situation, authority, deadline, evidence access and willingness to pay.

## Commercial evidence ladder
| Stage | Evidence required | Commercial status |
|---|---|---|
| Public issue discovered | Source URL and dated text | Problem context only |
| Decision relevance reviewed | Actual milestone/decision supported by source | Research candidate |
| Useful contribution | Accurate public answer actually posted | Contribution, not lead |
| Author engagement | Author responds or asks follow-up | Engagement, not buyer |
| Service inquiry | Author independently asks about service | Inbound interest |
| Qualified opportunity | Current consequential situation, decision owner, authority, permission and willingness to pay evidenced | Potential opportunity |
| Accepted engagement | Written scope, fee, timing and terms accepted | Contractual acceptance |
| Paid engagement | Advance receipt independently verified | Customer rupee |
| Earned revenue | Delivery and earned consideration evidenced | Earned rupee |

## Safeguards
No unsolicited DMs, mass mentions, promotional comments, requests for confidential records in public, inferred buying intent, or automated public posting under the owner's identity. Pricing, scope, contractual commitments and sensitive disclosures remain owner decisions.

## Acceptance criteria
Operational: scheduled run succeeds, source records are traceable, pagination and deduplication work, and unit tests pass.
Useful: reviewed candidates repeatedly contain real implementation lifecycle situations.
Commercially effective: channel contributes to consent-based qualified conversations and ultimately paid engagements.
These are separate claims and must be reported separately. Queue size, issue count, comments, stars and views are not success metrics.
