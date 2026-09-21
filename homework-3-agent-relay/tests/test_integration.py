"""End-to-end API integration test for Agent Relay task exchange.

Exercises the full lifecycle required by Homework 3 Question 2:
1. Register two agents (sender and recipient).
2. Sender submits a task addressed to recipient.
3. Recipient claims the queued task and receives a claim token.
4. Recipient processes and completes the task with output.
5. Sender verifies the task transitioned to 'completed' status.
"""

import os
import pytest
from fastapi.testclient import TestClient

import main
from database import Base, engine

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def register_agent(client: TestClient, name: str, description: str = "") -> tuple[str, dict[str, str]]:
    res = client.post("/api/v1/agents", json={"name": name, "description": description})
    assert res.status_code == 201, f"Failed to register agent {name}: {res.text}"
    data = res.json()
    agent_id = data["agent_id"]
    headers = {"Authorization": f"Bearer {data['token']}"}
    return agent_id, headers

def test_full_task_exchange_lifecycle():
    with TestClient(main.app) as client:
        # Step 1: Register sender and recipient agents
        sender_id, sender_headers = register_agent(client, "alice-sender", "Task initiator")
        worker_id, worker_headers = register_agent(client, "bob-worker", "Task processor")

        # Step 2: Sender creates a task for recipient
        task_payload = {
            "to": worker_id,
            "input": "Compute fibonacci(10) and return the value."
        }
        create_res = client.post(
            "/api/v1/tasks",
            headers={**sender_headers, "Idempotency-Key": "task-flow-1"},
            json=task_payload
        )
        assert create_res.status_code == 201
        created_task = create_res.json()
        task_id = created_task["task_id"]
        assert created_task["status"] == "queued"

        # Step 3: Recipient claims the task
        claim_res = client.post(
            "/api/v1/tasks/claim",
            headers=worker_headers,
            json={"worker_id": "bob-laptop-01", "wait_seconds": 5}
        )
        assert claim_res.status_code == 200
        claimed_task = claim_res.json()
        assert claimed_task["task_id"] == task_id
        assert claimed_task["from"] == sender_id
        claim_token = claimed_task["claim_token"]
        assert claim_token is not None

        # Verify task is now processing
        check_processing = client.get(f"/api/v1/tasks/{task_id}", headers=sender_headers)
        assert check_processing.status_code == 200
        assert check_processing.json()["status"] == "processing"

        # Step 4: Recipient completes the task with result
        result_payload = {
            "claim_token": claim_token,
            "output": "Result: 55"
        }
        complete_res = client.post(
            f"/api/v1/tasks/{task_id}/complete",
            headers=worker_headers,
            json=result_payload
        )
        assert complete_res.status_code == 200
        assert complete_res.json()["status"] == "completed"

        # Step 5: Sender checks task status - sender sees 'completed'
        final_check = client.get(f"/api/v1/tasks/{task_id}", headers=sender_headers)
        assert final_check.status_code == 200
        final_data = final_check.json()
        assert final_data["status"] == "completed"
        assert final_data["output"] == "Result: 55"
        assert final_data["finished_at"] is not None
