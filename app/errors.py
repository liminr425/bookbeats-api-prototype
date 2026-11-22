from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str, details=None):
        self.status = status
        self.code = code
        self.message = message
        self.details = details

def error_body(code, message, details=None):
    err = {"code": code, "message": message}
    if details:
        err["details"] = details
    return {"success": False, "error": err}

def register_handlers(app):
    @app.exception_handler(ApiError)
    async def api_error(request: Request, exc: ApiError):
        return JSONResponse(status_code=exc.status, content=error_body(exc.code, exc.message, exc.details))

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        details = [
            {"field": ".".join(str(p) for p in e["loc"] if p != "body"), "message": e["msg"]}
            for e in exc.errors()
        ]
        return JSONResponse(
            status_code=400,
            content=error_body("VALIDATION_ERROR", "The request contains invalid or missing fields.", details),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_error(request: Request, exc: StarletteHTTPException):
        codes = {404: "NOT_FOUND", 405: "METHOD_NOT_ALLOWED"}
        msgs = {404: "Resource not found.", 405: "Method not allowed for this endpoint."}
        return JSONResponse(
            status_code=exc.status_code,
            content=error_body(codes.get(exc.status_code, "ERROR"), msgs.get(exc.status_code, "Request failed.")),
        )

    @app.exception_handler(Exception)
    async def unexpected(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=error_body("INTERNAL_ERROR", "Something went wrong on the server."),
        )

def ok(message, data=None, meta=None):
    body = {"success": True, "message": message, "data": data}
    if meta:
        body["meta"] = meta
    return body