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


def fields(r):
    return {d["field"]: d["message"] for d in err(r, 400, "VALIDATION_ERROR")["details"]}


def post(body):
    return client.post("/api/v1/playlists", headers=A, json=body)


def test_missing_required_fields():
    assert {"title", "bookTitle", "mood", "songs"} <= set(fields(post({})))


def test_short_title():
    assert "title" in fields(post({**VALID, "title": "ab"}))


def test_whitespace_only_title_rejected():
    assert "title" in fields(post({**VALID, "title": "     "}))


def test_wrong_types_and_ranges():
    assert "intensity" in fields(post({**VALID, "intensity": "50"}))
    assert "intensity" in fields(post({**VALID, "intensity": 101}))


def test_bad_mood_and_empty_songs():
    assert "mood" in fields(post({**VALID, "mood": "angry"}))
    assert "songs" in fields(post({**VALID, "songs": []}))


def test_nested_song_error_path():
    assert "songs[0].artist" in fields(post({**VALID, "songs": [{"title": "x"}]}))


def test_unknown_and_ownerId_fields_rejected():
    f = fields(post({**VALID, "ownerId": "admin", "foo": 1}))
    assert f["ownerId"] == "Unknown field." and f["foo"] == "Unknown field."


def test_invalid_json_body():
    r = client.post("/api/v1/playlists", headers={**A, "Content-Type": "application/json"}, content="{bad")
    assert fields(r) == {"body": "Request body must be valid JSON."}


def test_bad_query_params():
    assert "page" in fields(client.get("/api/v1/playlists?page=0", headers=A))
    assert "perPage" in fields(client.get("/api/v1/playlists?perPage=500", headers=A))
    assert "mood" in fields(client.get("/api/v1/playlists?mood=angry", headers=A))


def test_put_validates_body_too():
    assert "title" in fields(client.put("/api/v1/playlists/pl_101", headers=A, json={**VALID, "title": "ab"}))
