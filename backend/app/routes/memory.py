from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.hindsight_client import get_hindsight_client
from app.config import settings

router = APIRouter()
hindsight = get_hindsight_client()

class RetainRequest(BaseModel):
    deal_id: str
    call_id: str
    content: str

class RecallRequest(BaseModel):
    deal_id: str
    query: str

@router.post("/retain")
def retain_memory(request: RetainRequest):
    try:
        metadata = {
            "deal_id": request.deal_id,
            "call_id": request.call_id
        }
        
        response = hindsight.retain(
            bank_id=settings.hindsight_bank_id,
            content=request.content,
            metadata=metadata
        )
        return {"status": "success", "message": "Memory retained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hindsight API Error: {str(e)}")

@router.post("/recall")
def recall_memory(request: RecallRequest):
    try:
        # A realistic implementation would use 'metadata' or 'tags' filtering for the specific deal_id
        # if Hindsight supported it directly in the query. Currently we append the deal_id to the query context.
        query = f"[Deal: {request.deal_id}] {request.query}"
        
        response = hindsight.recall(
            bank_id=settings.hindsight_bank_id,
            query=query
        )
        
        # Format response for the frontend
        memories = getattr(response, 'answers', getattr(response, 'results', []))
        if hasattr(response, 'answer'):
            # The API returns a direct answer sometimes
            memories = [{"text": response.answer}]

        return {
            "status": "success",
            "deal_id": request.deal_id,
            "recalled_memories": memories,
            "raw_response": response.model_dump() if hasattr(response, 'model_dump') else str(response)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hindsight API Error: {str(e)}")
