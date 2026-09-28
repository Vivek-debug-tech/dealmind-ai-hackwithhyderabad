// This object is what /api/prepare will eventually return for real.
// Keep this exact shape in mind when Person A builds the backend —
// changing this file's shape is the ONLY thing that should need to change
// when we swap mock data for the real API.

export const mockPrepareResponse = {
  deal_id: "DEAL-001",
  deal_name: "Acme Corp",
  owner: "Priya Nair",
  stage: "Negotiation",
  value: "$180K",
  segment: "Enterprise",

  risk: {
    level: "high",       // "low" | "medium" | "high"
    previous_level: "medium"
  },

  contradiction: {
    previous: "Budget isn't a blocker",
    current: "Budget may require scope reduction",
    detected_in: "Call 3",
    conflicts_with: "Call 1"
  },

  timeline: [
    {
      call: "Call 1",
      summary: "Pricing objection raised · mentioned Salesforce as alternative",
      flag: false
    },
    {
      call: "Call 2",
      summary: "Raised SAP integration as a technical concern",
      flag: false
    },
    {
      call: "Call 3",
      summary: "Budget concern resurfaces",
      flag: true
    }
  ],

  recommendation: {
    key_concern: "Budget pressure combined with unresolved SAP integration risk",
    suggested_question: "Would a phased rollout help fit this within the revised budget?",
    action: "Bring a scoped, lower-cost phase-1 proposal before discussing full pricing."
  }
};
