"""Public endpoint: the HTML greeting page and health check."""
from html import escape

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from .. import project_info as info
from ..errors import ok


router = APIRouter(prefix="/api/v1", tags=["system"])

_CSS = """
:root{--ink:#241b3f;--paper:#f7f5fc;--card:#fff;--line:#ddd7ee;--muted:#6a6385;--accent:#5b4bb7;--ok:#1f8a5b}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
header{background:var(--ink);color:#f3efff;padding:3rem 1.25rem 2.5rem}
.wrap{max-width:68rem;margin:0 auto}
h1{font:700 clamp(2.4rem,7vw,4rem)/1.05 "Iowan Old Style",Palatino,Georgia,serif;margin:0 0 .75rem;letter-spacing:-.01em}
header p{margin:0;max-width:40rem;color:#cfc7ea}
.status{display:inline-flex;align-items:center;gap:.5rem;margin-top:1.25rem;padding:.3rem .8rem;border:1px solid #4a3f78;border-radius:999px;font-size:.9rem}
.dot{width:.6rem;height:.6rem;border-radius:50%;background:#3ddc97}
main{padding:2rem 1.25rem 3rem}
.grid{display:grid;gap:2rem;grid-template-columns:1fr}
@media(min-width:56rem){.grid{grid-template-columns:20rem 1fr}}
h2{font:600 1.25rem/1.3 "Iowan Old Style",Palatino,Georgia,serif;margin:0 0 .75rem}
.member{padding:.9rem 0;border-top:1px solid var(--line)}
.member b{display:block}.member small{color:var(--muted)}
.member p{margin:.25rem 0 0}
.endpoint{display:grid;grid-template-columns:4.5rem 1fr;gap:.25rem .75rem;padding:.8rem 0;border-top:1px solid var(--line)}
.m{font:700 .78rem/1.6 ui-monospace,Menlo,Consolas,monospace;text-align:center;border-radius:.3rem;padding:0 .3rem;height:1.5rem;color:#fff}
.GET{background:#2f7fc1}.POST{background:var(--ok)}.PUT{background:#c0801a}.DELETE{background:#b53b52}
code{font:.92rem ui-monospace,Menlo,Consolas,monospace;word-break:break-all}
.desc{grid-column:2;color:var(--muted);font-size:.93rem}
.tag{font-size:.75rem;color:var(--accent);border:1px solid var(--line);border-radius:.3rem;padding:0 .35rem;margin-left:.4rem;white-space:nowrap}
footer{color:var(--muted);font-size:.85rem;margin-top:2rem}
""".strip()


def _render() -> str:
    team = "".join(
        f'<div class="member"><b>{escape(m["name"])}</b><small>Student ID: {escape(m["student_id"])}</small>'
        f'<p>{escape(m["built"])}</p></div>' for m in info.TEAM)
    endpoints = "".join(
        f'<div class="endpoint"><span class="m {m}">{m}</span>'
        f'<span><code>{escape(p)}</code><span class="tag">{escape(a)}</span></span>'
        f'<span class="desc">{escape(d)}</span></div>' for m, p, d, a in info.ENDPOINTS)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(info.PROJECT_NAME)} API</title>
<style>{_CSS}</style>
</head>
<body>
<header><div class="wrap">
<h1>Welcome to {escape(info.PROJECT_NAME)}</h1>
<p>{escape(info.DESCRIPTION)}</p>
<div class="status"><span class="dot"></span>API is running &middot; version {escape(info.API_VERSION)}</div>
</div></header>
<main><div class="wrap grid">
<section><h2>Team</h2>{team}</section>
<section><h2>Available endpoints</h2>{endpoints}
<footer>Protected endpoints need the header <code>Authorization: Bearer &lt;token&gt;</code>.</footer></section>
</div></main>
</body>
</html>"""


@router.get("/greeting", response_class=HTMLResponse)
def greeting():
    return HTMLResponse(_render(), media_type="text/html; charset=utf-8")


@router.get("/health")
def health():
    return ok("BookBeats API is running.", {"status": "ok", "version": info.API_VERSION})