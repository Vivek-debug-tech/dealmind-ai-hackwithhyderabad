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

@router.post("/comparison")
def compare_preparation(request: PrepareRequest):
    # WITHOUT MEMORY
    try:
        without_memory = analyzer.analyze_deal(memories=[], query=request.query)
    except Exception as e:
        logger.error(f"Without Memory Analysis Error: {e}")
        without_memory = {"error": "Failed to analyze without memory"}

    # WITH HINDSIGHT
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
            with_hindsight_analysis = analyzer.analyze_deal(memories=memories, query=request.query)
            with_hindsight = {
                **with_hindsight_analysis,
                "memories_used": [{"text": mem, "source": "Hindsight"} for mem in memories]
            }
        except Exception as e:
            logger.error(f"With Hindsight Analysis Error: {e}")
            with_hindsight = {"error": "Failed to analyze with hindsight"}

    return {
        "status": "success",
        "deal_id": request.deal_id,
        "without_memory": without_memory,
        "with_hindsight": with_hindsight
    }
