"""CRUD for the `playlists` resource (a saved BookBeats playlist - FR-06)."""
from typing import Optional

from fastapi import APIRouter, Depends, Query

from .. import data as store
from ..auth import current_user
from ..errors import ApiError, ok
from ..schemas import Mood

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


@router.get("")
def list_playlists(
    user: dict = Depends(current_user),
    page: int = Query(1, ge=1),
    perPage: int = Query(10, ge=1, le=50),
    mood: Optional[Mood] = Query(None),
    q: Optional[str] = Query(None, min_length=1, max_length=100),
):
    owner_filter = None if user["role"] == "admin" else user["id"]
    items = store.list_all(owner_id=owner_filter, mood=mood, q=q)
    start = (page - 1) * perPage
    return ok("Playlists retrieved successfully.", items[start:start + perPage],
              {"total": len(items), "page": page, "perPage": perPage})