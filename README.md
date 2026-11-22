# BookBeats API

BookBeats turns any book into a custom soundtrack. This repository is the first backend prototype:
a REST API built with **Python + FastAPI**, using **mocked in-memory data** instead of PostgreSQL.
The main resource is `playlists` (saved playlists).

Team **DoubleL**: Leyla Khanaliyeva, Liaman Shakhbazova.
Course: CSCI 3509, Intro to Software Engineering.

## Install and run

Requires Python 3.10+.

```bash
git clone https://github.com/liminr425/bookbeats-api-prototype.git
cd bookbeats-api-prototype
python3 -m venv .venv            # on Windows use: python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/api/v1/greeting> in a browser.

> **Mock data:** all data lives in memory and **resets every time the server restarts**.
