# DealMind AI Backend

This is the backend for DealMind AI, implementing the Hindsight memory layer.

## Setup Instructions

### 1. Create and Activate Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the `backend/` directory by copying `.env.example`:
```bash
cp .env.example .env
```
Edit `.env` and manually insert the actual `HINDSIGHT_API_KEY`. (Do not commit this file!)

### 4. Start FastAPI
```bash
uvicorn app.main:app --reload
```

## Testing

### 1. Test /health Endpoint
```bash
curl http://127.0.0.1:8000/health
# Expected: {"status": "ok"}
```

### 2. Test Retain Memory
```bash
curl -X POST http://127.0.0.1:8000/api/memory/retain \
     -H "Content-Type: application/json" \
     -d '{
       "deal_id": "DEAL-001",
       "call_id": "CALL-001",
       "content": "Acme is comparing DealMind with Salesforce. The buyer said budget is not currently a blocker."
     }'
```

### 3. Test Recall Memory
```bash
curl -X POST http://127.0.0.1:8000/api/memory/recall \
     -H "Content-Type: application/json" \
     -d '{
       "deal_id": "DEAL-001",
       "query": "What concerns and objections have Acme stakeholders raised?"
     }'
```
