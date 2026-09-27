# DealMind AI — Primary Demo Scenario

## Prospect

**Acme Technologies**

- Deal ID: DEAL-001
- Industry: SaaS
- Deal Size: $180,000
- Stage: Negotiation

---

## Demo Objective

Demonstrate how persistent memory allows DealMind to prepare a sales representative using information from multiple historical interactions with the same prospect.

The demonstration should show that the agent becomes more specific when historical context is available.

---

## Call 1 — Pricing and Competitor

**Call ID:** CALL-001

Acme says that DealMind's pricing is higher than Salesforce.

### Important memories

- Pricing is an objection.
- Salesforce is a competitor.
- Budget is initially not considered a blocker.

---

## Call 2 — Technical Integration

**Call ID:** CALL-002

Acme's CTO raises concerns about integrating the solution with the company's existing SAP environment.

### Important memories

- SAP integration is a technical concern.
- Potential customization effort is a concern.
- Additional integration information was requested.

---

## Call 3 — Budget Change

**Call ID:** CALL-003

Acme's CFO explains that the budget situation has changed.

Earlier:

> Budget was not considered a blocker.

Later:

> We may need to reduce the project scope because of budget.

### Important memories

- Budget has become a concern.
- Project scope may need to be reduced.
- Phased implementation may be required.

---

# Critical Contradiction

The customer's position on budget changed during the sales cycle.

### Earlier signal

Budget was not considered a blocker.

### Later signal

Budget may require reducing the project scope.

### Expected interpretation

Deal risk has increased because the customer's commercial position changed.

---

# Live Demo Sequence

## Step 1 — Introduce the prospect

Show Acme Technologies and the $180,000 deal.

## Step 2 — Show historical interaction

Show Call 1.

Highlight:

- Pricing objection
- Salesforce competitor

## Step 3 — Add technical context

Show Call 2.

Highlight:

- SAP integration concern

## Step 4 — Add latest commercial context

Show Call 3.

Highlight:

- Budget position changed
- Possible scope reduction

## Step 5 — Ask DealMind

Sales representative asks:

> "Prepare me for my call with Acme."

## Step 6 — Memory Recall

DealMind should retrieve relevant historical context.

The response should include:

- Pricing concern
- Salesforce competitor
- SAP integration concern
- Previous budget position
- Latest budget signal

## Step 7 — Contradiction Detection

DealMind should identify that Acme's budget position changed.

## Step 8 — Updated Deal Risk

DealMind should identify increased deal risk related to budget.

## Step 9 — Recommended Action

DealMind should recommend:

1. Discussing a phased implementation.
2. Identifying essential capabilities for Phase 1.
3. Addressing the pricing concern.
4. Providing the requested SAP integration information.

---

# Expected Before/After

## Without Historical Memory

The agent may provide generic sales preparation advice.

Example:

> Review the customer's requirements, understand their concerns, and prepare a product demonstration.

## With Historical Memory

The agent should provide prospect-specific preparation.

Example:

> Acme previously raised concerns about pricing compared with Salesforce and SAP integration. Their latest conversation also indicates that budget has become a potential blocker, despite the earlier position that budget was not a concern. Prepare to discuss phased implementation, prioritize Phase 1 capabilities, and address the pricing and integration concerns.

---

# Success Condition

The demo succeeds when the audience can clearly see that remembering previous interactions changes the agent's recommendation.

The goal is not simply to show that DealMind can generate an email.

The goal is to demonstrate:

**Past interaction → Memory → New information → Contradiction → Updated deal context → Action**