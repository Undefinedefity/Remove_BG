from __future__ import annotations

import base64
import os
from datetime import date
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Tuple

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image

# Ensure numba (used by rembg) can write its cache somewhere writable.
_default_cache_path = Path(__file__).resolve().parent / ".numba_cache"
_configured_cache = os.environ.get("NUMBA_CACHE_DIR")

if _configured_cache:
    Path(_configured_cache).mkdir(parents=True, exist_ok=True)
else:
    _default_cache_path.mkdir(exist_ok=True)
    os.environ["NUMBA_CACHE_DIR"] = str(_default_cache_path)

from rembg import remove

app = FastAPI(title="RemoveBG Web")
templates = Jinja2Templates(directory="templates")

AUTHOR_NAME = "Def"
APP_VERSION = "v1.0.0"
UPDATE_HISTORY: List[Dict[str, str]] = [
    {"date": "2025-11-07", "detail": "Added interactive brush controls for manual refine."},
    {"date": "2025-11-07", "detail": "Initial FastAPI web UI for removing backgrounds."},
]


def _encode_png(image_bytes: bytes) -> str:
    """Return a data URL for embedding the PNG in HTML."""
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def _to_png_bytes(image_bytes: bytes) -> Tuple[bytes, Tuple[int, int]]:
    """Convert arbitrary bytes to RGBA PNG bytes and return the rendered size."""
    with Image.open(BytesIO(image_bytes)) as img:
        rgba = img.convert("RGBA")
        buffer = BytesIO()
        rgba.save(buffer, format="PNG")
        return buffer.getvalue(), rgba.size


def _base_context() -> Dict[str, Any]:
    last_updated = UPDATE_HISTORY[0]["date"] if UPDATE_HISTORY else date.today().isoformat()
    return {
        "author_name": AUTHOR_NAME,
        "last_updated": last_updated,
        "app_version": APP_VERSION,
        "update_history": UPDATE_HISTORY,
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    context = {
        **_base_context(),
        "request": request,
        "result_image": None,
    }
    return templates.TemplateResponse("index.html", context)


@app.post("/remove", response_class=HTMLResponse)
async def remove_background(request: Request, file: UploadFile = File(...)) -> HTMLResponse:
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file.")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        output = remove(image_bytes)
    except Exception as exc:  # pragma: no cover - rembg internal errors
        raise HTTPException(status_code=500, detail="Background removal failed.") from exc

    result_data_url = _encode_png(output)
    original_png_bytes, _ = _to_png_bytes(image_bytes)
    original_data_url = _encode_png(original_png_bytes)
    context: Dict[str, Any] = {
        **_base_context(),
        "request": request,
        "result_image": result_data_url,
        "file_name": file.filename or "result.png",
        "original_image": original_data_url,
    }
    return templates.TemplateResponse("index.html", context)
