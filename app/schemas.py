from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field

Mood = Literal["dark", "tense", "dreamy", "nostalgic", "calm",
               "uplifting", "romantic", "mysterious", "energetic"]


class Song(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=120)
    artist: str = Field(min_length=1, max_length=120)


class PlaylistInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)

    title: str = Field(min_length=3, max_length=100)
    bookTitle: str = Field(min_length=1, max_length=150)
    bookAuthor: Optional[str] = Field(default=None, min_length=1, max_length=100)
    mood: Mood
    intensity: int = Field(default=50, ge=0, le=100)
    songs: list[Song] = Field(min_length=1, max_length=20)
