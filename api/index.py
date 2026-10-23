import sys
import os
import urllib.parse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi import Request

# Ensure backend directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
backend_dir = os.path.join(root_dir, "backend")

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app
from app.core.database import db_manager

# Ensure health endpoints are directly available
@app.get("/health", tags=["Health"])
@app.get("/api/health", tags=["Health"])
@app.get("/api/v1/health", tags=["Health"])
def health_endpoint():
    conn_info = db_manager.check_connection()
    return {
        "status": "healthy" if conn_info["connected"] else "degraded",
        "mongodb": conn_info
    }

# Frontend static files configuration
dist_dir = os.path.join(root_dir, "frontend", "dist")
assets_dir = os.path.join(dist_dir, "assets")

if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

@app.get("/favicon.svg")
def get_favicon():
    fav_path = os.path.join(dist_dir, "favicon.svg")
    if os.path.exists(fav_path):
        return FileResponse(fav_path)
    return JSONResponse(status_code=404, content={"detail": "Not found"})

@app.get("/icons.svg")
def get_icons():
    icon_path = os.path.join(dist_dir, "icons.svg")
    if os.path.exists(icon_path):
        return FileResponse(icon_path)
    return JSONResponse(status_code=404, content={"detail": "Not found"})

@app.get("/index.html")
def get_index():
    index_path = os.path.join(dist_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(status_code=404, content={"detail": "Index not found"})

# SPA fallback handler for any remaining route
@app.get("/{full_path:path}")
def spa_fallback(full_path: str):
    index_path = os.path.join(dist_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(status_code=404, content={"detail": f"Path {full_path} not found"})

class VercelPathCorrectionMiddleware:
    """
    ASGI middleware that extracts the rewritten _path parameter from Vercel edge
    and updates scope['path'] so FastAPI routers match correctly.
    """
    def __init__(self, asgi_app):
        self.asgi_app = asgi_app

    async def __call__(self, scope, receive, send):
        if scope["type"] in ("http", "websocket"):
            qs = scope.get("query_string", b"").decode("latin1", errors="ignore")
            if "_path=" in qs:
                params = urllib.parse.parse_qs(qs, keep_blank_values=True)
                if "_path" in params and params["_path"]:
                    target_path = params["_path"][0]
                    del params["_path"]
                    # Rebuild clean query string without _path
                    clean_qs = urllib.parse.urlencode(params, doseq=True)
                    scope["query_string"] = clean_qs.encode("latin1")
                    scope["path"] = target_path
                    scope["raw_path"] = target_path.encode("latin1")

        await self.asgi_app(scope, receive, send)

# Wrap app with the path correction middleware
app = VercelPathCorrectionMiddleware(app)
handler = app
