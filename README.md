# Remove Background Web App

Simple FastAPI-based web UI for removing image backgrounds using [rembg](https://github.com/danielgatis/rembg).

## Setup

1. Create virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the development server:

```bash
uvicorn app:app --reload
```

4. Open your browser at <http://127.0.0.1:8000> and upload an image.

## Notes

- Output is delivered as a transparent PNG embedded in the page with a download link.
- Large images may take a few seconds depending on your CPU/GPU.
