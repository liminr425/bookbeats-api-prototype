from fastapi import FastAPI
from .errors import register_handlers
from .routes import playlists, greeting

app = FastAPI(title="BookBeats API", version="v1")
register_handlers(app)
app.include_router(greeting.router)
app.include_router(playlists.router)