# BookBeats API (Assignment 2 prototype)

BookBeats turns any book into a custom soundtrack. This repository is the first backend prototype:
a REST API built with **Python + FastAPI**, using **mocked in-memory data** instead of PostgreSQL.
The main resource is `playlists` (saved playlists).

Team **DoubleL**: Leyla Khanaliyeva and Liaman Shakhbazova.
ADA University, CSCI 3509: Intro to Software Engineering, CRN 10938

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

## Mock users

| Role | Header |
|---|---|
| User A | `Authorization: Bearer user-a-token` |
| User B | `Authorization: Bearer user-b-token` |
| Admin | `Authorization: Bearer admin-token` |

## Try it

```bash
curl http://127.0.0.1:8000/api/v1/playlists -H "Authorization: Bearer user-a-token"
```

More examples: [`examples/requests.http`](examples/requests.http) (VS Code "REST Client" extension, or copy the curl equivalents from [API.md](API.md)).

## Documentation

Full endpoint documentation, error codes and the 404-vs-403 design decision: [API.md](API.md).

## Tests

```bash
python -m pytest
```

## Project structure

```
app/
  main.py            app setup
  auth.py            mock tokens and the current_user dependency (401)
  schemas.py         request validation rules
  data.py            in-memory mock data
  errors.py          response envelope and global error handlers
  project_info.py    team/project text shown on the greeting page
  routes/
    playlists.py     CRUD + ownership rules
    greeting.py      HTML greeting page and health check
tests/              automated tests for every status code
examples/requests.http
```
