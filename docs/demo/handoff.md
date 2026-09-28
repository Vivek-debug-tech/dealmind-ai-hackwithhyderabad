# DealMind AI — Person B Handoff

## Primary Demo

**Prospect:** Acme Technologies  
**Deal ID:** DEAL-001  
**Industry:** SaaS  
**Deal Size:** $180,000  
**Stage:** Negotiation

The Acme Technologies deal is the primary Hindsight memory demonstration.

---

## Historical Interaction Sequence

### CALL-001 — Discovery Call

**Date:** 2026-09-20

Key memories:

- Acme considers the proposed pricing significantly higher than Salesforce.
- Salesforce is being considered as a competing solution.
- Sarah Mitchell indicated that budget was not currently a blocker.

**Memory importance:** High

---

### CALL-002 — Technical Evaluation

**Date:** 2026-09-23

Key memories:

- David Chen identified SAP integration as the primary technical concern.
- Acme wants to understand the required customization and integration effort.
- Additional integration information was committed.

**Memory importance:** High

---

### CALL-003 — Commercial Review

**Date:** 2026-09-26

Key memories:

- Michael Roberts reported that Acme's budget situation had changed.
- Acme may need to reduce project scope because of budget constraints.
- Acme asked about phased implementation.
- Essential capabilities may need to be prioritized for Phase 1.

**Memory importance:** Critical

---

## Critical Memory Contradiction

### Earlier Signal

> Budget was not considered a blocker.

Source: CALL-001

### Later Signal

> Acme may need to reduce the project scope because of budget.

Source: CALL-003

### Expected Memory Behavior

DealMind should recognize that the customer's budget position changed during the sales cycle.

The latest signal should affect the current deal assessment.

Expected consequence:

**Deal risk increases.**

---

## Final Demo Query

The sales representative asks:

> Prepare me for my call with Acme.

---

## Expected Agent Response

The agent should use historical memory to identify:

1. Pricing is a concern.
2. Salesforce is a competitor.
3. SAP integration is a technical concern.
4. Budget was initially not considered a blocker.
5. The latest budget signal changed that position.
6. The budget change represents an important contradiction/update.
7. Current deal risk has increased.
8. A phased implementation should be discussed.
9. Essential capabilities should be prioritized for Phase 1.

---

## Hindsight Memory Goal

The demonstration should show that historical interactions change the usefulness of the response.

### Without historical memory

The agent has insufficient context about Acme's previous concerns.

### With historical memory

The agent can connect:

**pricing → competitor → SAP integration → budget change → increased risk → recommended action**

The key demonstration is that the agent does not treat the latest conversation as isolated.

---

## Files Used

Primary prospect:

`data/prospects/acme.json`

Demo definition:

`docs/demo/primary_demo.json`

Full demo narrative:

`docs/demo/demo_scenario.md`

Additional prospects:

`data/prospects/novaretail.json`

`data/prospects/finedge.json`

---

## Handoff to Person A

Person A should use the Acme call history as the primary Hindsight memory demonstration.

The three calls should be stored/recalled as chronological historical interactions.

The final query is:

> Prepare me for my call with Acme.

The desired result is a preparation response grounded in the historical interactions, including recognition of the changed budget signal and its impact on deal risk.