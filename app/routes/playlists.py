"""CRUD for the `playlists` resource (a saved BookBeats playlist - FR-06)."""
from fastapi import APIRouter

from .. import data as store
from ..errors import ApiError

router = APIRouter(prefix="/api/v1/playlists", tags=["playlists"])


def _find_accessible(playlist_id: str, user: dict) -> dict:
    """Return the playlist, or 404 if it doesn't exist OR belongs to someone else.

    Using the same 404 for both cases means a regular user cannot even discover
    that another user's playlist exists (see API.md, 'Why 404 instead of 403').
    """
    playlist = store.get(playlist_id)
    if playlist is None or (user["role"] != "admin" and playlist["ownerId"] != user["id"]):
        raise ApiError(404, "NOT_FOUND", "Playlist not found.")
    return playlist