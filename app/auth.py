from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .errors import ApiError

TOKENS = {
    "user-a-token": {"id": "user-a", "role": "user"},
    "user-b-token": {"id": "user-b", "role": "user"},
    "admin-token":  {"id": "admin",  "role": "admin"},
}

bearer = HTTPBearer(auto_error=False)

def current_user(creds: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if creds is None:
        raise ApiError(401, "UNAUTHORIZED", "Authorization token is missing.")
    user = TOKENS.get(creds.credentials)
    if user is None:
        raise ApiError(401, "UNAUTHORIZED", "Authorization token is invalid.")
    return user