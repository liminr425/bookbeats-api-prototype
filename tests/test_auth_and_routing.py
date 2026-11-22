import pytest
from fastapi.testclient import TestClient

from app import data
from app.main import app

client = TestClient(app)
A = {"Authorization": "Bearer user-a-token"}
ADMIN = {"Authorization": "Bearer admin-token"}


@pytest.fixture(autouse=True)
def fresh_data():
    data.reset()


def err(r, status, code):
    assert r.status_code == status, r.text
    body = r.json()
    assert body["success"] is False and body["error"]["code"] == code
    return body["error"]


# ---- authentication ----
def test_missing_token_401():
    err(client.get("/api/v1/playlists"), 401, "UNAUTHORIZED")


def test_invalid_token_401():
    err(client.get("/api/v1/playlists", headers={"Authorization": "Bearer nope"}), 401, "UNAUTHORIZED")


def test_wrong_scheme_401():
    err(client.get("/api/v1/playlists", headers={"Authorization": "Basic user-a-token"}), 401, "UNAUTHORIZED")


def test_auth_is_checked_before_validation():
    err(client.post("/api/v1/playlists", json={}), 401, "UNAUTHORIZED")


# ---- list: meta, pagination, filters ----
def test_list_meta():
    assert client.get("/api/v1/playlists", headers=A).json()["meta"] == {"total": 2, "page": 1, "perPage": 10}


def test_pagination():
    r = client.get("/api/v1/playlists?page=2&perPage=2", headers=ADMIN).json()
    assert len(r["data"]) == 2 and r["meta"] == {"total": 5, "page": 2, "perPage": 2}


def test_filter_by_mood_and_search():
    assert client.get("/api/v1/playlists?mood=tense", headers=ADMIN).json()["meta"]["total"] == 1
    assert client.get("/api/v1/playlists?q=dune", headers=ADMIN).json()["meta"]["total"] == 1


# ---- routing errors ----
def test_405_keeps_allow_header():
    r = client.patch("/api/v1/playlists/pl_101", headers=A, json={})
    err(r, 405, "METHOD_NOT_ALLOWED")
    assert "allow" in r.headers


def test_unknown_route_404():
    err(client.get("/api/v1/nothing"), 404, "NOT_FOUND")


# ---- greeting and health ----
def test_greeting_is_html_with_project_info():
    r = client.get("/api/v1/greeting")
    assert r.status_code == 200
    assert r.headers["content-type"] == "text/html; charset=utf-8"
    assert "Welcome to BookBeats" in r.text and "/api/v1/playlists/{id}" in r.text and "viewport" in r.text


