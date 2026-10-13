def payload(**overrides):
    data = {"problem_id":"parking-lot","learner_id":"learner-test",
      "classes":[
        {"name":"ParkingLot","responsibility":"Coordinates spot allocation and tracks parking inventory."},
        {"name":"ParkingTicket","responsibility":"Records entry time and the spot assigned for one visit."},
        {"name":"FeeCalculator","responsibility":"Calculates the fee using duration and a pricing policy."}],
      "relationships_text":"ParkingLot owns many ParkingSpot objects and creates a ParkingTicket. FeeCalculator uses a closed ticket and pricing policy.",
      "patterns":"Strategy pattern lets pricing policies share an interface and change without modifying ticket logic.",
      "tradeoffs":"An in-memory allocator is simple for a demo. Database transactions or locks prevent double-booking under concurrent entry.",
      "edge_cases":"If the lot is full, reject entry. If a ticket is invalid or already closed, do not charge twice."}
    data.update(overrides); return data

def test_health_and_seeded_problems(client):
    assert client.get("/api/health").json() == {"status":"ok"}
    response = client.get("/api/problems")
    assert response.status_code == 200 and len(response.json()) >= 3

def test_problem_not_found(client):
    assert client.get("/api/problems/nope").status_code == 404

def test_submission_has_explainable_feedback(client):
    response = client.post("/api/attempts", json=payload())
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "evaluated" and 0 <= body["score"] <= 100
    assert len(body["feedback"]["dimensions"]) == 5

def test_history_scoped_to_learner(client):
    client.post("/api/attempts", json=payload())
    assert len(client.get("/api/problems/parking-lot/attempts?learner_id=learner-test").json()) == 1
    assert client.get("/api/problems/parking-lot/attempts?learner_id=other").json() == []

def test_invalid_submission_rejected(client):
    data = payload()
    data["classes"] = [{"name":"X","responsibility":"tiny"}]
    assert client.post("/api/attempts", json=data).status_code == 422

def test_unknown_problem_rejected(client):
    assert client.post("/api/attempts", json=payload(problem_id="unknown")).status_code == 404

def test_unknown_attempt_rejected(client):
    assert client.get("/api/attempts/9999").status_code == 404

def test_retry_conflict_for_successful_evaluation(client):
    attempt = client.post("/api/attempts", json=payload()).json()
    assert client.post(f"/api/attempts/{attempt['id']}/retry-evaluation").status_code == 409
