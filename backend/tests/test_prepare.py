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

    response = client.post("/api/prepare/comparison", json={
        "deal_id": "DEAL-001",
        "query": "Prepare me."
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["without_memory"] == expected_analysis
    assert data["with_hindsight"]["prospect"] == "Acme"
    assert len(data["with_hindsight"]["memories_used"]) == 1
    
    # Hindsight should be called exactly once
    mock_hindsight.assert_called_once()
    
    # Groq should be called exactly twice (once without memory, once with)
    assert mock_groq_client.call_count == 2
    # Verify first call had empty memories
    mock_groq_client.assert_any_call(memories=[], query="Prepare me.")

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
