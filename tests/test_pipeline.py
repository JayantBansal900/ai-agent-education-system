from fastapi.testclient import TestClient

from backend.agents.reviewer import reviewer_agent
from backend.main import app

client = TestClient(app)

GOOD_MCQ = {"question": "Q?", "options": ["a", "b", "c", "d"], "answer": "a"}


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200


def test_generate_returns_draft_and_review():
    response = client.post("/generate", json={"grade": 5, "topic": "Angles"})
    assert response.status_code == 200
    body = response.json()
    assert "explanation" in body["initial"]
    assert body["review"]["status"] in {"pass", "fail"}


def test_generate_validates_input():
    response = client.post("/generate", json={"grade": "five"})
    assert response.status_code == 422


def test_reviewer_passes_good_content():
    content = {"explanation": "Angles are made by two lines.", "mcqs": [GOOD_MCQ, GOOD_MCQ]}
    assert reviewer_agent(content, 5) == {"status": "pass", "feedback": []}


def test_reviewer_flags_long_explanation():
    content = {"explanation": "word " * 101, "mcqs": [GOOD_MCQ, GOOD_MCQ]}
    assert reviewer_agent(content, 5)["status"] == "fail"


def test_reviewer_flags_complex_words():
    content = {"explanation": "Consequently, angles exist.", "mcqs": [GOOD_MCQ, GOOD_MCQ]}
    feedback = reviewer_agent(content, 3)["feedback"]
    assert any("consequently" in item for item in feedback)


def test_reviewer_flags_too_few_mcqs():
    content = {"explanation": "Short.", "mcqs": [GOOD_MCQ]}
    assert "Not enough MCQs" in reviewer_agent(content, 5)["feedback"]


def test_reviewer_flags_wrong_option_count():
    bad = {"question": "Q?", "options": ["a", "b"], "answer": "a"}
    content = {"explanation": "Short.", "mcqs": [GOOD_MCQ, bad]}
    assert "MCQ 2 must have 4 options" in reviewer_agent(content, 5)["feedback"]
