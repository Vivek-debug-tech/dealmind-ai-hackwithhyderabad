import os
import pytest
from unittest.mock import patch, MagicMock

# Set mock env vars before imports
os.environ["HINDSIGHT_API_KEY"] = "test_key"
os.environ["GROQ_API_KEY"] = "test_groq"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_hindsight():
    with patch("app.routes.prepare.hindsight.recall") as mock:
        yield mock

@pytest.fixture
def mock_groq_client():
    with patch("app.services.deal_analyzer.DealAnalyzer.analyze_deal") as mock:
        yield mock

def test_prepare_validation():
    # Missing deal_id
    response = client.post("/api/prepare", json={"query": "test"})
    assert response.status_code == 422

    # Missing query
    response = client.post("/api/prepare", json={"deal_id": "123"})
    assert response.status_code == 422

def test_prepare_empty_memory(mock_hindsight):
    # Mock Hindsight returning empty results
    mock_resp = MagicMock()
    mock_resp.answers = []
    mock_hindsight.return_value = mock_resp

    response = client.post("/api/prepare", json={
        "deal_id": "DEAL-001",
        "query": "Prepare me for Acme."
    })
    
    assert response.status_code == 404
    assert "No historical memories found" in response.json()["detail"]

def test_prepare_groq_failure(mock_hindsight, mock_groq_client):
    # Setup Hindsight to return a memory
    mock_resp = MagicMock()
    mock_ans = MagicMock()
    mock_ans.text = "Some memory"
    mock_resp.answers = [mock_ans]
    mock_hindsight.return_value = mock_resp

    # Setup Groq to raise an error
    mock_groq_client.side_effect = RuntimeError("Groq is down")

    response = client.post("/api/prepare", json={
        "deal_id": "DEAL-001",
        "query": "Prepare me for Acme."
    })
    
    assert response.status_code == 500
    assert "Failed to analyze deal history" in response.json()["detail"]

def test_prepare_invalid_json(mock_hindsight, mock_groq_client):
    mock_resp = MagicMock()
    mock_ans = MagicMock()
    mock_ans.text = "Some memory"
    mock_resp.answers = [mock_ans]
    mock_hindsight.return_value = mock_resp

    # Setup Groq to raise ValueError (simulating JSONDecodeError inside analyzer)
    mock_groq_client.side_effect = ValueError("LLM returned malformed JSON.")

    response = client.post("/api/prepare", json={
        "deal_id": "DEAL-001",
        "query": "Prepare me for Acme."
    })
    
    assert response.status_code == 500
    assert "LLM returned malformed JSON" in response.json()["detail"]

def test_prepare_success_and_budget_change(mock_hindsight, mock_groq_client):
    mock_resp = MagicMock()
    mock_ans1 = MagicMock()
    mock_ans1.text = "Acme said budget is not a blocker."
    mock_ans2 = MagicMock()
    mock_ans2.text = "Acme said budget is now a concern and requires scope reduction."
    mock_resp.answers = [mock_ans1, mock_ans2]
    mock_hindsight.return_value = mock_resp

    # Mock the returned JSON structure from Groq
    expected_analysis = {
        "prospect": "Acme",
        "deal_summary": "Acme deal.",
        "risk": {"level": "MEDIUM", "reason": "Budget cuts"},
        "key_concerns": ["Budget"],
        "changes_detected": [
            {
                "topic": "Budget",
                "previous_position": "Not a blocker",
                "current_position": "Requires scope reduction",
                "significance": "Could reduce deal size"
            }
        ],
        "contradictions": [],
        "recommended_questions": ["What is the new budget limit?"],
        "recommended_actions": ["Review scope"]
    }
    mock_groq_client.return_value = expected_analysis

    response = client.post("/api/prepare", json={
        "deal_id": "DEAL-001",
        "query": "Prepare me for Acme."
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["deal_id"] == "DEAL-001"
    assert data["prospect"] == "Acme"
    assert len(data["changes_detected"]) == 1
    assert data["changes_detected"][0]["topic"] == "Budget"
    assert len(data["memories_used"]) == 2
    assert "not a blocker" in data["memories_used"][0]["text"]

def test_comparison_success(mock_hindsight, mock_groq_client):
    # Mock Hindsight
    mock_resp = MagicMock()
    mock_ans = MagicMock()
    mock_ans.text = "Acme memory"
    mock_resp.answers = [mock_ans]
    mock_hindsight.return_value = mock_resp

    # Mock Groq logic - we can differentiate by checking the memories argument but 
    # to keep it simple we'll just let it return the same mocked dict
    expected_analysis = {"prospect": "Acme", "deal_summary": "Analysis"}
    mock_groq_client.return_value = expected_analysis

    with patch("app.routes.prepare.get_latest_crm_context") as mock_crm:
        crm_note = "[Current CRM Note - 2026-09-26] Commercial Review: budget changed."
        mock_crm.return_value = crm_note
        
        response = client.post("/api/prepare/comparison", json={
            "deal_id": "DEAL-001",
            "query": "Prepare me."
        })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["without_memory"] == expected_analysis
    assert data["with_hindsight"]["prospect"] == "Acme"
    
    # Prove that both results are returned
    assert "without_memory" in data
    assert "with_hindsight" in data
    
    # Hindsight should be called twice (cross-deal and scoped)
    assert mock_hindsight.call_count == 2
    
    # Groq should be called exactly twice (once without memory, once with)
    assert mock_groq_client.call_count == 2
    
    # Verify first call (without_memory) received the latest CRM context only
    mock_groq_client.assert_any_call(memories=[crm_note], query="Prepare me.")
    
    # Verify second call (with_hindsight) received BOTH the latest CRM context AND Hindsight memory
    # Because cross-deal is also called, it might get cross_deal_memories kwargs
    # We just check the memories list
    args, kwargs = mock_groq_client.call_args_list[1]
    assert kwargs["memories"] == [crm_note, "Acme memory"]

def test_cross_deal_learning(mock_hindsight, mock_groq_client):
    # Mock Hindsight side_effect for the 2 calls: cross-deal then scoped recall
    mock_resp_cross = MagicMock()
    mock_ans_cross = MagicMock()
    mock_ans_cross.text = "[Deal: DEAL-002] outcome: WON, objection: budget, tactic: phased rollout"
    # To test DEAL-001 exclusion, include a DEAL-001 memory in cross-deal response
    mock_ans_cross2 = MagicMock()
    mock_ans_cross2.text = "[Deal: DEAL-001] some memory"
    mock_resp_cross.answers = [mock_ans_cross, mock_ans_cross2]
    
    mock_resp_scoped = MagicMock()
    mock_ans_scoped = MagicMock()
    mock_ans_scoped.text = "Acme scoped memory"
    mock_resp_scoped.answers = [mock_ans_scoped]
    
    mock_hindsight.side_effect = [mock_resp_cross, mock_resp_scoped]

    expected_analysis = {
        "prospect": "Acme", 
        "deal_summary": "Analysis",
        "similar_deals": {
            "count": 1,
            "evidence": "Phased rollout worked",
            "deals": [{"deal_id": "DEAL-002", "outcome": "WON", "tactic": "phased rollout"}]
        }
    }
    mock_groq_client.return_value = expected_analysis

    with patch("app.routes.prepare.get_latest_crm_context") as mock_crm:
        mock_crm.return_value = ""
        response = client.post("/api/prepare/comparison", json={
            "deal_id": "DEAL-001",
            "query": "Prepare me."
        })
    
    assert response.status_code == 200
    data = response.json()
    assert "with_hindsight" in data
    assert data["with_hindsight"]["similar_deals"]["count"] == 1
    
    # Check Hindsight was called twice
    assert mock_hindsight.call_count == 2
    # First call for cross-deal
    args1, kwargs1 = mock_hindsight.call_args_list[0]
    assert "DEAL-001" not in kwargs1["query"]
    assert "budget objections" in kwargs1["query"]
    
    # Second call for scoped
    args2, kwargs2 = mock_hindsight.call_args_list[1]
    assert "[Deal: DEAL-001]" in kwargs2["query"]
    
    # Verify DEAL-001 was filtered out of cross_deal_memories passed to Groq
    groq_args, groq_kwargs = mock_groq_client.call_args_list[1]
    cross_deal_mems = groq_kwargs.get("cross_deal_memories")
    assert len(cross_deal_mems) == 1
    assert "DEAL-002" in cross_deal_mems[0]
    assert "DEAL-001" not in cross_deal_mems[0]

def test_cross_deal_no_results(mock_hindsight, mock_groq_client):
    mock_resp_empty = MagicMock()
    mock_resp_empty.answers = []
    
    mock_resp_scoped = MagicMock()
    mock_ans = MagicMock()
    mock_ans.text = "Acme memory"
    mock_resp_scoped.answers = [mock_ans]
    
    mock_hindsight.side_effect = [mock_resp_empty, mock_resp_scoped]

    expected_analysis = {
        "prospect": "Acme", 
        "similar_deals": {
            "count": 0,
            "evidence": "No relevant past deals found.",
            "deals": []
        }
    }
    mock_groq_client.return_value = expected_analysis

    with patch("app.routes.prepare.get_latest_crm_context") as mock_crm:
        mock_crm.return_value = ""
        response = client.post("/api/prepare/comparison", json={
            "deal_id": "DEAL-001",
            "query": "Prepare me."
        })
    
    assert response.status_code == 200
    data = response.json()
    assert data["with_hindsight"]["similar_deals"]["count"] == 0
    
    groq_args, groq_kwargs = mock_groq_client.call_args_list[1]
    cross_deal_mems = groq_kwargs.get("cross_deal_memories")
    assert len(cross_deal_mems) == 0

def test_comparison_groq_failure_handled_safely(mock_hindsight, mock_groq_client):
    mock_resp = MagicMock()
    mock_ans = MagicMock()
    mock_ans.text = "Acme memory"
    mock_resp.answers = [mock_ans]
    mock_hindsight.return_value = mock_resp

    # Groq fails
    mock_groq_client.side_effect = ValueError("Malformed JSON")

    response = client.post("/api/prepare/comparison", json={
        "deal_id": "DEAL-001",
        "query": "Prepare me."
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "error" in data["without_memory"]
    assert "error" in data["with_hindsight"]
