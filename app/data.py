import itertools
from copy import deepcopy
from datetime import datetime, timezone
from typing import Optional

def _song(title, artist):
    return {"title": title, "artist": artist}

def _seed() -> dict:
    rows = [
        ("pl_1", "user-a", "Gone Girl Nights", "Gone Girl", "Gillian Flynn", "tense", 80,
         [_song("Everything In Its Right Place", "Radiohead"), _song("Seven Nation Army", "The White Stripes"),
          _song("Heathens", "Twenty One Pilots")]),
        ("pl_2", "user-a", "Gatsby Summer", "The Great Gatsby", "F. Scott Fitzgerald", "nostalgic", 40,
         [_song("Young and Beautiful", "Lana Del Rey"), _song("Video Games", "Lana Del Rey"),
          _song("Dreams", "Fleetwood Mac")]),
        ("pl_3", "user-b", "Pride & Piano", "Pride and Prejudice", "Jane Austen", "romantic", 30,
         [_song("Clair de Lune", "Claude Debussy"), _song("Gymnopédie No. 1", "Erik Satie"),
          _song("La Vie en Rose", "Édith Piaf")]),
        ("pl_4", "user-b", "Arrakis Soundtrack", "Dune", "Frank Herbert", "mysterious", 70,
         [_song("Time", "Hans Zimmer"), _song("Tubular Bells", "Mike Oldfield"),
          _song("Shine On You Crazy Diamond", "Pink Floyd")]),
          ("pl_105", "admin", "Admin Pick: The Hobbit", "The Hobbit", "J. R. R. Tolkien", "uplifting", 60,
         [_song("Here Comes the Sun", "The Beatles"), _song("Rivers and Roads", "The Head and the Heart"),
          _song("Home", "Edward Sharpe & The Magnetic Zeros")]),
    ]

    data = {}
    for i, (pid, owner, title, book, author, mood, intensity, songs) in enumerate(rows):
        stamp = f"2026-11-0{i + 1}T10:00:00Z"
        data[pid] = {"id": pid, "title": title, "bookTitle": book, "bookAuthor": author, "mood": mood,
                     "intensity": intensity, "songs": songs, "ownerId": owner,
                     "createdAt": stamp, "updatedAt": stamp}
    return data

_playlists: dict = {}
_ids = itertools.count(106)

def reset() -> None:
    global _playlists, _ids
    _playlists = _seed()
    _ids = itertools.count(106)

reset()

def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def list_all(owner_id: Optional[str] = None, mood: Optional[str] = None, q: Optional[str] = None) -> list:
    items = list(_playlists.values())
    if owner_id:
        items = [p for p in items if p["ownerId"] == owner_id]
    if mood:
        items = [p for p in items if p["mood"] == mood]
    if q:
        needle = q.lower()
        items = [p for p in items if needle in p["title"].lower() or needle in p["bookTitle"].lower()]
    return deepcopy(items)

def get(playlist_id: str) -> Optional[dict]:
    p = _playlists.get(playlist_id)
    return deepcopy(p) if p else None

def title_taken(owner_id: str, title: str, exclude_id: Optional[str] = None) -> bool:
    return any(p["ownerId"] == owner_id and p["title"].lower() == title.lower() and p["id"] != exclude_id
               for p in _playlists.values())

def create(owner_id: str, data: dict) -> dict:
    pid = f"pl_{next(_ids)}"
    now = _now()
    _playlists[pid] = {"id": pid, **data, "ownerId": owner_id, "createdAt": now, "updatedAt": now}
    return deepcopy(_playlists[pid])

def replace(playlist_id: str, data: dict) -> dict:
    current = _playlists[playlist_id]
    _playlists[playlist_id] = {"id": playlist_id, **data, "ownerId": current["ownerId"],
                               "createdAt": current["createdAt"], "updatedAt": _now()}
    return deepcopy(_playlists[playlist_id])

def delete(playlist_id: str) -> None:
    del _playlists[playlist_id]