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


def test_list_only_own():
    r = client.get("/api/v1/playlists", headers=A)
    assert r.status_code == 200
    body = r.json()
    assert {p["ownerId"] for p in body["data"]} == {"user-a"}
    assert body["meta"]["total"] == 2


def test_admin_sees_all():
    assert client.get("/api/v1/playlists", headers=ADMIN).json()["meta"]["total"] == 5


def test_get_own_ok_and_admin_ok():
    assert client.get("/api/v1/playlists/pl_101", headers=A).status_code == 200
    assert client.get("/api/v1/playlists/pl_101", headers=ADMIN).status_code == 200


@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_cross_user_access_is_404(method):
    kwargs = {"json": VALID} if method == "put" else {}
    err(getattr(client, method)("/api/v1/playlists/pl_103", headers=A, **kwargs), 404, "NOT_FOUND")
    err(getattr(client, method)("/api/v1/playlists/pl_101", headers=B, **kwargs), 404, "NOT_FOUND")


def test_admin_can_update_and_delete_any_playlist():
    assert client.put("/api/v1/playlists/pl_103", headers=ADMIN, json=VALID).status_code == 200
    assert client.delete("/api/v1/playlists/pl_104", headers=ADMIN).status_code == 200


def test_nonexistent_id_404():
    err(client.get("/api/v1/playlists/pl_999", headers=A), 404, "NOT_FOUND")


def test_owner_filter_forbidden_for_user_but_ok_for_admin():
    err(client.get("/api/v1/playlists?ownerId=user-b", headers=A), 403, "FORBIDDEN")
    assert client.get("/api/v1/playlists?ownerId=user-b", headers=ADMIN).json()["meta"]["total"] == 2
