# LovePrompt

LovePrompt converts PDFs, DOCX, PPTX, TXT, and other files into clean Markdown optimized for LLMs (Claude, ChatGPT, etc.) using [Microsoft MarkItDown](https://github.com/microsoft/markitdown).

## Features

- Drag-and-drop upload UI (React + Vite)
- Markdown preview
- Token estimation
- Prompt optimization (whitespace cleanup for prompt-ready context)
- FastAPI API
- CLI conversion support
- Markdown export
- Preserves structure via MarkItDown (tables, headings, lists, code blocks)
- Dockerized API + frontend

## Project structure

- `/backend` – FastAPI service + CLI + tests
- `/frontend` – React UI
- `docker-compose.yml` – run API + UI together

## Run locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

CLI usage:

```bash
cd backend
python cli.py /path/to/document.pdf -o output.md
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Set API URL if needed:

```bash
VITE_API_URL=http://localhost:8000 npm run dev
```

## Docker

```bash
docker compose up --build
```

- API: `http://localhost:8000`
- UI: `http://localhost:5173`
