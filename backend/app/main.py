from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from .services import convert_file_to_markdown, estimate_tokens, optimize_markdown

app = FastAPI(title="LovePrompt API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConvertResponse(BaseModel):
    filename: str
    markdown: str
    optimized_markdown: str
    estimated_tokens: int


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/convert", response_model=ConvertResponse)
async def convert_document(file: UploadFile = File(...)) -> ConvertResponse:
    suffix = Path(file.filename or "document").suffix
    if not suffix:
        raise HTTPException(status_code=400, detail="Uploaded file must include an extension")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp_path = Path(tmp.name)
        tmp.write(await file.read())

    try:
        markdown = convert_file_to_markdown(tmp_path)
        optimized = optimize_markdown(markdown)
        tokens = estimate_tokens(optimized)
        return ConvertResponse(
            filename=file.filename or tmp_path.name,
            markdown=markdown,
            optimized_markdown=optimized,
            estimated_tokens=tokens,
        )
    except Exception as exc:  # pragma: no cover - framework error path
        raise HTTPException(status_code=400, detail=f"Unable to convert document: {exc}") from exc
    finally:
        tmp_path.unlink(missing_ok=True)


@app.post("/api/export", response_class=PlainTextResponse)
def export_markdown(payload: ConvertResponse) -> PlainTextResponse:
    stem = Path(payload.filename).stem or "document"
    return PlainTextResponse(
        payload.optimized_markdown,
        headers={"Content-Disposition": f'attachment; filename="{stem}.md"'},
    )
