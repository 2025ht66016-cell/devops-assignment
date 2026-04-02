import pytest

from app import create_app
from src.Aceestver import calculate_calories, get_program_by_code, get_programs_summary


# ── business logic ────────────────────────────────────────────────────────────

def test_program_lookup_is_case_insensitive():
    program = get_program_by_code("fl")
    assert program is not None
    assert program["name"] == "Fat Loss"


def test_program_summary_exposes_three_profiles():
    summaries = get_programs_summary()
    assert len(summaries) == 3
    assert {p["code"] for p in summaries} == {"FL", "MG", "BG"}


def test_program_summary_includes_calorie_factor():
    summaries = get_programs_summary()
    for p in summaries:
        assert "calorie_factor" in p
        assert p["calorie_factor"] > 0


def test_unknown_program_code_returns_none():
    assert get_program_by_code("XX") is None


@pytest.mark.parametrize("code,weight,expected", [
    ("FL", 70, 70 * 22),
    ("MG", 80, 80 * 35),
    ("BG", 60, 60 * 26),
])
def test_calculate_calories(code, weight, expected):
    assert calculate_calories(code, weight) == expected


def test_calculate_calories_unknown_program_returns_none():
    assert calculate_calories("XX", 70) is None


def test_calculate_calories_zero_weight_returns_none():
    assert calculate_calories("FL", 0) is None


# ── API endpoints ─────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    return create_app().test_client()


def test_health_endpoint_returns_ok_status(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"service": "aceest-fitness", "status": "ok"}


def test_program_list_endpoint_returns_expected_payload(client):
    response = client.get("/api/programs")
    payload = response.get_json()
    assert response.status_code == 200
    assert len(payload["programs"]) == 3


def test_program_detail_endpoint_returns_program_data(client):
    response = client.get("/api/programs/MG")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["code"] == "MG"
    assert payload["diet"].startswith("B: 4 Eggs")


def test_program_detail_endpoint_returns_404_for_unknown_program(client):
    response = client.get("/api/programs/xyz")
    assert response.status_code == 404
    assert "not found" in response.get_json()["error"].lower()


def test_calories_endpoint_returns_correct_estimate(client):
    response = client.post("/api/calories", json={"program_code": "FL", "weight_kg": 70})
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["estimated_calories"] == 70 * 22
    assert payload["program_code"] == "FL"


def test_calories_endpoint_missing_fields_returns_400(client):
    response = client.post("/api/calories", json={"program_code": "FL"})
    assert response.status_code == 400


def test_calories_endpoint_unknown_program_returns_404(client):
    response = client.post("/api/calories", json={"program_code": "XX", "weight_kg": 70})
    assert response.status_code == 404
