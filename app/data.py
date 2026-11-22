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
          _song("Shine On You Crazy Diamond", "Pink Floyd")])
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