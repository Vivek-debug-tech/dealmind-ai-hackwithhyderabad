import json
import logging
from typing import List, Dict, Any
from groq import Groq
from app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an elite sales intelligence analyst for DealMind AI.
Your objective is to analyze a chronology of sales-call memories for a specific deal, incorporate evidence from similar past deals, and prepare the sales representative for their next call.

CRITICAL INSTRUCTIONS:
1. Reason CHRONOLOGICALLY based only on the supplied memories. Do not hallucinate facts.
2. Distinguish between mere updates/changes vs. genuine contradictions.
   - Example of a change: "Budget was open, now it is tight." (Record in changes_detected)
   - Example of a contradiction: "Stakeholder A said they use AWS. Stakeholder B said they are 100% Azure." (Record in contradictions)
3. Assess the current deal risk realistically based on the latest information. Prioritize the most recent credible deal signals while still reporting earlier contradictory signals.
4. If there is a combination of negative signals such as a budget reversal (e.g., budget was open but is now constrained), unresolved technical integration risks (e.g., SAP), and competitive pricing pressure, the deal risk MUST be evaluated as HIGH. Explain exactly how these factors collectively increase deal risk in the risk reason.
5. Keep output actionable, concise, and focused on helping the rep close the deal.
6. If evidence is missing for a field, leave it empty or indicate "Unknown".
7. Analyze any provided Cross-Deal Memories (historical closed deals). If relevant past deals are found, summarize the tactical evidence in `similar_deals.evidence` and list the deals. Do NOT invent historical evidence or hallucinate successful tactics. If no relevant deals are found, set count to 0 and evidence to "No relevant past deals found."

OUTPUT FORMAT:
You MUST output valid JSON only, with the following exact structure:
{
  "prospect": "Company Name",
  "deal_summary": "Brief 2-3 sentence overview of the current deal state.",
  "risk": {
    "level": "LOW|MEDIUM|HIGH",
    "reason": "Why?"
  },
  "key_concerns": ["Concern 1", "Concern 2"],
  "changes_detected": [
    {
      "topic": "e.g., Budget",
      "previous_position": "What was said earlier",
      "current_position": "What is said now",
      "significance": "Why this matters"
    }
  ],
  "contradictions": [
    {
      "topic": "e.g., Timeline",
      "earlier_statement": "...",
      "later_statement": "...",
      "why_it_matters": "..."
    }
  ],
  "recommended_questions": ["Question 1", "Question 2"],
  "recommended_actions": ["Action 1", "Action 2"],
  "similar_deals": {
    "count": 2,
    "evidence": "A phased rollout resolved budget objections in 1 of 2 similar deals.",
    "deals": [
      {
        "deal_id": "DEAL-002",
        "outcome": "WON",
        "tactic": "phased rollout"
      }
    ]
  }
}
"""

class DealAnalyzer:
    def __init__(self):
        # We handle missing keys gracefully in routes, but the client needs the key
        self.client = None
        if settings.groq_api_key and settings.groq_api_key != "your_groq_api_key_here":
            self.client = Groq(api_key=settings.groq_api_key)

    def analyze_deal(self, memories: List[str], query: str, cross_deal_memories: List[str] = None) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("GROQ_API_KEY is not configured.")

        # Construct the user message
        if not memories:
            memories_text = "No historical memories available. Provide generic preparation."
        else:
            memories_text = "\n\n".join(f"[Memory {i+1}]: {mem}" for i, mem in enumerate(memories))
            
        cross_deal_text = ""
        if cross_deal_memories:
            cross_deal_text = "\n\nCROSS-DEAL MEMORIES (Historical Closed Deals):\n" + "\n\n".join(f"[Past Deal {i+1}]: {mem}" for i, mem in enumerate(cross_deal_memories))

        user_message = f"USER QUERY: {query}\n\nSALES CALL MEMORIES (Chronological):\n{memories_text}{cross_deal_text}\n\nProvide the required JSON analysis."

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ],
                model=settings.groq_model,
                response_format={"type": "json_object"},
                temperature=0.2, # Low temperature for more analytical/consistent output
            )

            raw_response = chat_completion.choices[0].message.content
            return json.loads(raw_response)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON output: {e}")
            raise ValueError("LLM returned malformed JSON.")
        except Exception as e:
            logger.error(f"Groq API Error: {e}")
            raise RuntimeError(f"Failed to perform LLM analysis: {str(e)}")

# Singleton instance
analyzer = DealAnalyzer()
