"""Single place to edit the project/team info shown on the greeting page."""

PROJECT_NAME = "BookBeats"
API_VERSION = "v1"
DESCRIPTION = ("BookBeats turns any book into a custom soundtrack. Readers type a book title and the system "
               "builds a playlist that matches its mood and genre, then saves it for later. "
               "It is built for readers, book clubs and music lovers.")

# TODO: replace the student IDs and adjust the summaries to match what each of you actually built.
TEAM = [
    {"name": "Liaman Shakhbazova", "student_id": "21425",
     "built": "Project skeleton, mock token authentication, error handling, list and get playlist endpoints, greeting page and routing tests."},
    {"name": "Leyla Khanaliyeva", "student_id": "17147",
     "built": "Mock data, validation, create/update/delete endpoints, ownership and validation tests, API docs and README."},
]

# (method, path, description, access)
ENDPOINTS = [
    ("GET", "/api/v1/greeting", "This page.", "Public"),
    ("GET", "/api/v1/health", "Health check used for monitoring.", "Public"),
    ("GET", "/api/v1/playlists", "List playlists (own only; admin sees all). Supports page, perPage, mood, q.", "Token"),
    ("GET", "/api/v1/playlists/{id}", "Get one playlist.", "Token"),
    ("POST", "/api/v1/playlists", "Create a playlist.", "Token"),
    ("PUT", "/api/v1/playlists/{id}", "Replace an existing playlist.", "Token"),
    ("DELETE", "/api/v1/playlists/{id}", "Delete a playlist.", "Token"),
]