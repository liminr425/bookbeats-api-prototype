import pytest
from fastapi.testclient import TestClient

from app import data
from app.main import app

client = TestClient(app)
A = {"Authorization": "Bearer user-a-token"}
B = {"Authorization": "Bearer user-b-token"}
ADMIN = {"Authorization": "Bearer admin-token"}

VALID = {"title": "Dune Focus", "bookTitle": "Dune", "mood": "mysterious", "intensity": 55,
         "songs": [{"title": "Time", "artist": "Hans Zimmer"}]}


@pytest.fixture(autouse=True)
def fresh_data():
    data.reset()


def err(r, status, code):
    assert r.status_code == status, r.text
    body = r.json()
    assert body["success"] is False and body["error"]["code"] == code
    return body["error"]


def test_create_201_and_owner_is_caller():
    r = client.post("/api/v1/playlists", headers=A, json=VALID)
    assert r.status_code == 201
    created = r.json()["data"]
    assert created["ownerId"] == "user-a" and created["id"] == "pl_106"
    assert client.get("/api/v1/playlists/pl_106", headers=A).status_code == 200


def test_create_defaults_intensity_to_50():
    body = {k: v for k, v in VALID.items() if k != "intensity"}
    assert client.post("/api/v1/playlists", headers=A, json=body).json()["data"]["intensity"] == 50


def test_duplicate_title_409_but_other_user_ok():
    client.post("/api/v1/playlists", headers=A, json=VALID)
    err(client.post("/api/v1/playlists", headers=A, json=VALID), 409, "CONFLICT")
    assert client.post("/api/v1/playlists", headers=B, json=VALID).status_code == 201


def test_put_replaces_and_keeps_owner():
    r = client.put("/api/v1/playlists/pl_101", headers=ADMIN, json=VALID)
    assert r.status_code == 200
    d = r.json()["data"]
    assert d["title"] == "Dune Focus" and d["ownerId"] == "user-a" and d["createdAt"] == "2026-11-01T10:00:00Z"


def test_put_own_title_ok_but_other_playlists_title_conflicts():
    same = {**VALID, "title": "Gone Girl Nights"}
    assert client.put("/api/v1/playlists/pl_101", headers=A, json=same).status_code == 200
    err(client.put("/api/v1/playlists/pl_102", headers=A, json=same), 409, "CONFLICT")


def test_put_nonexistent_404():
    err(client.put("/api/v1/playlists/pl_999", headers=A, json=VALID), 404, "NOT_FOUND")


def test_delete_then_gone():
    r = client.delete("/api/v1/playlists/pl_101", headers=A)
    assert r.status_code == 200 and r.json()["data"] is None
    err(client.get("/api/v1/playlists/pl_101", headers=A), 404, "NOT_FOUND")


def test_delete_nonexistent_404():
    err(client.delete("/api/v1/playlists/pl_999", headers=A), 404, "NOT_FOUND")
