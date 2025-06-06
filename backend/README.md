# Orchids Website Cloner Backend

This backend powers the AI Website Cloner using FastAPI, a custom scraper, and Anthropic's Claude 3 Opus for HTML generation.

## Requirements
- Python 3.9+
- `pip` (Python package manager)
- Anthropic Claude API key

## Setup

1. **Clone the repository and enter the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install python-dotenv aiohttp
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and add your Anthropic API key:
     ```bash
     cp .env.example .env
     # Edit .env and set ANTHROPIC_API_KEY=your-key-here
     ```

## Running the Backend

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Endpoints
- `POST /clone` — Start a website cloning job (provide `{ "url": "https://example.com" }`)
- `GET /clone/{job_id}` — Get the status and result of a cloning job
- `GET /api/health` — Health check

## Notes
- The backend uses Anthropic Claude 3 Opus for HTML generation. Make sure your API key is valid and you have access to the model.
- For production, use a persistent database instead of in-memory job storage. 