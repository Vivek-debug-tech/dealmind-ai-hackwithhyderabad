from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

from app.hindsight_client import get_hindsight_client
from app.services.deal_analyzer import analyzer
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()
hindsight = get_hindsight_client()

class PrepareRequest(BaseModel):
    deal_id: str
    query: str
    mode: str = "both"  # "both", "without_memory", "with_hindsight"

@router.post("")
def prepare_for_call(request: PrepareRequest):
    # 1. Recall relevant Hindsight memories for the deal
    try:
        # Contextualize query with deal_id for scoped retrieval
        scoped_query = f"[Deal: {request.deal_id}] {request.query}"
        hindsight_resp = hindsight.recall(
            bank_id=settings.hindsight_bank_id,
            query=scoped_query
        )
        
        # Extract memories safely
        memories = []
        if hasattr(hindsight_resp, 'answers') and hindsight_resp.answers:
            memories = [ans.text if hasattr(ans, 'text') else str(ans) for ans in hindsight_resp.answers]
        elif hasattr(hindsight_resp, 'results') and hindsight_resp.results:
            memories = [res.text if hasattr(res, 'text') else str(res) for res in hindsight_resp.results]
        elif hasattr(hindsight_resp, 'answer'):
            memories = [hindsight_resp.answer]
            
    except Exception as e:
        logger.error(f"Hindsight Recall Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve deal history from Hindsight.")

    # If no memories found, we can't analyze
    if not memories:
        raise HTTPException(status_code=404, detail="No historical memories found for this deal.")

    # 2. Analyze the chronological history using the LLM through Groq
    try:
        analysis_result = analyzer.analyze_deal(memories=memories, query=request.query)
        
        # 3. Combine with standard envelope and return
        return {
            "status": "success",
            "deal_id": request.deal_id,
            **analysis_result,
            "memories_used": [
                {"text": mem, "source": "Hindsight"} for mem in memories
            ]
        }
        
    except ValueError as e:
        # Configuration or parsing issues
        logger.error(f"Analysis ValueError: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis RuntimeError: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze deal history.")

import os
import json

def get_latest_crm_context(deal_id: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "data", "prospects"))
    if not os.path.exists(data_dir):
        return ""
    
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    deal_data = json.load(f)
                    if deal_data.get("deal_id") == deal_id:
                        calls = deal_data.get("calls", [])
                        if calls:
                            latest_call = calls[-1]
                            return f"[Current CRM Note - {latest_call.get('date', 'Unknown')}] {latest_call.get('type', '')}: {latest_call.get('transcript', '')}"
            except Exception as e:
                logger.error(f"Error reading local deal data {filepath}: {e}")
                pass
    return ""

@router.post("/comparison")
def compare_preparation(request: PrepareRequest):
    latest_context = get_latest_crm_context(request.deal_id)
    without_memories = [latest_context] if latest_context else []
    
    response = {
        "status": "success",
        "deal_id": request.deal_id,
        "without_memory": None,
        "with_hindsight": None
    }

    # WITHOUT MEMORY
    if request.mode in ["both", "without_memory"]:
        try:
            response["without_memory"] = analyzer.analyze_deal(memories=without_memories, query=request.query)
        except Exception as e:
            logger.error(f"Without Memory Analysis Error: {e}")
            response["without_memory"] = {"error": "Failed to analyze without memory"}

    # WITH HINDSIGHT
    if request.mode in ["both", "with_hindsight"]:
        cross_deal_memories = []
        try:
            cross_deal_query = f"closed deals budget objections pricing pressure tactics outcomes {request.query}"
            cd_resp = hindsight.recall(
                bank_id=settings.hindsight_bank_id,
                query=cross_deal_query
            )
            cd_items = []
            if hasattr(cd_resp, 'answers') and cd_resp.answers:
                cd_items = cd_resp.answers
            elif hasattr(cd_resp, 'results') and cd_resp.results:
                cd_items = cd_resp.results
            elif hasattr(cd_resp, 'answer'):
                cd_items = [{"text": cd_resp.answer}]
                
            for item in cd_items:
                text = item.text if hasattr(item, 'text') else (item.get("text") if isinstance(item, dict) else str(item))
                if f"[Deal: {request.deal_id}]" not in text:
                    cross_deal_memories.append(text)
        except Exception as e:
            logger.error(f"Hindsight Cross-Deal Recall Error: {e}")

        memories = []
        try:
            scoped_query = f"[Deal: {request.deal_id}] {request.query}"
            hindsight_resp = hindsight.recall(
                bank_id=settings.hindsight_bank_id,
                query=scoped_query
            )
            
            if hasattr(hindsight_resp, 'answers') and hindsight_resp.answers:
                memories = [ans.text if hasattr(ans, 'text') else str(ans) for ans in hindsight_resp.answers]
            elif hasattr(hindsight_resp, 'results') and hindsight_resp.results:
                memories = [res.text if hasattr(res, 'text') else str(res) for res in hindsight_resp.results]
            elif hasattr(hindsight_resp, 'answer'):
                memories = [hindsight_resp.answer]
                
        except Exception as e:
            logger.error(f"Hindsight Recall Error in comparison: {e}")
            with_hindsight = {"error": "Failed to retrieve deal history"}
        
        if not memories and 'with_hindsight' not in locals():
            with_hindsight = {"error": "No historical memories found for this deal."}
        elif 'with_hindsight' not in locals():
            try:
                with_memories = []
                if latest_context:
                    with_memories.append(latest_context)
                with_memories.extend(memories)

                with_hindsight_analysis = analyzer.analyze_deal(
                    memories=with_memories, 
                    query=request.query, 
                    cross_deal_memories=cross_deal_memories
                )
                
                memories_used = []
                for i, mem in enumerate(with_memories):
                    source = "CRM" if (latest_context and i == 0) else "Hindsight"
                    memories_used.append({"text": mem, "source": source})
                    
                with_hindsight = {
                    **with_hindsight_analysis,
                    "memories_used": memories_used
                }
            except Exception as e:
                logger.error(f"With Hindsight Analysis Error: {e}")
                with_hindsight = {"error": "Failed to analyze with hindsight"}

        response["with_hindsight"] = with_hindsight

    return response
