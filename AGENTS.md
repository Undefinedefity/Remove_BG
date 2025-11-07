# Repository Guidelines

## Project Structure & Module Organization
- `app.py` hosts the FastAPI app, rembg integration, and helper utilities (PNG encoding, numba cache prep).
- `templates/index.html` contains the single-page UI with the brush editor script.
- `static/` is reserved for future assets; `README.md` and `AGENTS.md` document the project.
- Temporary artifacts such as `.numba_cache/` and `__pycache__/` are ignored via `.gitignore`.

## Build, Test, and Development Commands
- `conda activate remove-bg` & `pip install -r requirements.txt` — set up the Python 3.11 environment with FastAPI, rembg, and onnxruntime.
- `uvicorn app:app --reload` — launch the development server with hot reload (falls back to plain `uvicorn app:app` if file watching is blocked).
- `python -m pip check` — optional sanity check for dependency conflicts after upgrades.

## Coding Style & Naming Conventions
- Stick to Python 3.11+, PEP 8 spacing, and descriptive snake_case names for functions (`_encode_png`, `_base_context`).
- Keep templates in HTML5 with inline CSS; prefer BEM-like class names when styling new components.
- Place configuration constants (e.g., `AUTHOR_NAME`, `APP_VERSION`) near the top of `app.py`.
- When touching the JS editor, keep functions small and favor early returns for readability.

## Testing Guidelines
- Currently manual QA: run `uvicorn app:app`, upload varied PNG/JPEG files, and validate brush edits (restore/erase/reset/download).
- If you add automated tests, use `pytest` under `tests/` and name files `test_<feature>.py`.
- Capture regressions around mask editing by comparing resulting PNG alphas where feasible.

## Commit & Pull Request Guidelines
- Follow conventional commits (e.g., `feat:`, `fix:`, `docs:`) as used in the history (`feat: add interactive brush editor`, `docs: add footer metadata`).
- Each PR should describe the UI/UX impact, include screenshots for front-end changes, and reference related issues.
- Ensure branches are rebased on `main`, CI (if added) passes, and new commands/config updates are reflected in `README.md` and `AGENTS.md`.

## Security & Configuration Tips
- Do not hard-code secrets; rembg runs locally and only needs default configs.
- Respect `NUMBA_CACHE_DIR` overrides to avoid permission problems on hosted environments.
