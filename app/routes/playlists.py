"""CRUD for the `playlists` resource (a saved BookBeats playlist - FR-06)."""
from typing import Optional

from fastapi import APIRouter, Depends, Query

from .. import data as store
from ..auth import current_user
from ..errors import ApiError, ok
from ..schemas import Mood, PlaylistInput

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

def _check_title_free(owner_id: str, title: str, exclude_id: Optional[str] = None) -> None:
    if store.title_taken(owner_id, title, exclude_id):
        raise ApiError(409, "CONFLICT", f"A playlist titled '{title}' already exists for this user.")

@router.get("")
def list_playlists(
    user: dict = Depends(current_user),
    page: int = Query(1, ge=1),
    perPage: int = Query(10, ge=1, le=50),
    mood: Optional[Mood] = Query(None),
    q: Optional[str] = Query(None, min_length=1, max_length=100),
    ownerId: Optional[str] = Query(None, min_length=1, max_length=50),
):
    if ownerId is not None and user["role"] != "admin":
        raise ApiError(403, "FORBIDDEN", "Only administrators can filter playlists by owner.")
    owner_filter = ownerId if user["role"] == "admin" else user["id"]
    items = store.list_all(owner_id=owner_filter, mood=mood, q=q)
    start = (page - 1) * perPage
    return ok("Playlists retrieved successfully.", items[start:start + perPage],
              {"total": len(items), "page": page, "perPage": perPage})

@router.get("/{playlist_id}")
def get_playlist(playlist_id: str, user: dict = Depends(current_user)):
    return ok("Playlist retrieved successfully.", _find_accessible(playlist_id, user))

@router.post("", status_code=201)
def create_playlist(payload: PlaylistInput, user: dict = Depends(current_user)):
    data = payload.model_dump()
    _check_title_free(user["id"], data["title"])
    return ok("Playlist created successfully.", store.create(user["id"], data))

@router.put("/{playlist_id}")
def update_playlist(playlist_id: str, payload: PlaylistInput, user: dict = Depends(current_user)):
    existing = _find_accessible(playlist_id, user)
    data = payload.model_dump()
    _check_title_free(existing["ownerId"], data["title"], exclude_id=playlist_id)
    return ok("Playlist updated successfully.", store.replace(playlist_id, data))

@router.delete("/{playlist_id}")
def delete_playlist(playlist_id: str, user: dict = Depends(current_user)):
    _find_accessible(playlist_id, user)
    store.delete(playlist_id)
    return ok("Playlist deleted successfully.", None)