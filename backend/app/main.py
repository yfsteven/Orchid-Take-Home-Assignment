from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
import asyncio
import aiohttp
import base64
import json
import os
from datetime import datetime
import uuid
from .scraper import WebScraper
from .llm import LLMGenerator
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
scraper = WebScraper()
try:
    llm_generator = LLMGenerator()  # Using hardcoded API key
    logger.info("LLMGenerator initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize LLMGenerator: {str(e)}")
    raise

app = FastAPI(
    title="AI Website Cloner API",
    description="API for cloning website aesthetics using LLM",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class CloneRequest(BaseModel):
    url: str
    output_dir: Optional[str] = "output"
    
class CloneResponse(BaseModel):
    job_id: str
    status: str
    message: str

class CloneStatus(BaseModel):
    id: str
    status: str
    progress: int
    message: str
    html: Optional[str] = None
    error: Optional[str] = None

# In-memory storage (in production, use Redis or database)
clone_jobs: Dict[str, Dict[str, Any]] = {}

@app.get("/")
async def root():
    return {"message": "Website Cloner API", "status": "running"}

@app.post("/clone", response_model=CloneResponse)
async def clone_website(request: CloneRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    clone_jobs[job_id] = {
        "id": job_id,
        "status": "queued",
        "progress": 0,
        "message": "Job queued",
        "html": None,
        "error": None
    }
    background_tasks.add_task(process_clone_job, job_id, request.url, request.output_dir)
    return CloneResponse(
        job_id=job_id,
        status="queued",
        message="Cloning started in background"
    )

@app.get("/clone/{job_id}", response_model=CloneStatus)
async def get_clone_status(job_id: str):
    if job_id not in clone_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    job = clone_jobs[job_id]
    return CloneStatus(
        id=job["id"],
        status=job["status"],
        progress=job["progress"],
        message=job["message"],
        html=job.get("html"),
        error=job.get("error")
    )

def process_clone_job(job_id: str, url: str, output_dir: str):
    try:
        clone_jobs[job_id]["status"] = "scraping"
        clone_jobs[job_id]["progress"] = 10
        clone_jobs[job_id]["message"] = "Scraping website..."
        scraped_data = scraper.scrape_website(url)

        clone_jobs[job_id]["status"] = "generating"
        clone_jobs[job_id]["progress"] = 50
        clone_jobs[job_id]["message"] = "Generating code with LLM..."
        generated_code = llm_generator.generate_website_code(scraped_data)

        clone_jobs[job_id]["status"] = "saving"
        clone_jobs[job_id]["progress"] = 80
        clone_jobs[job_id]["message"] = "Saving generated code..."
        llm_generator.save_generated_code(generated_code, output_dir)

        clone_jobs[job_id]["status"] = "completed"
        clone_jobs[job_id]["progress"] = 100
        clone_jobs[job_id]["message"] = "Website cloned successfully."
        clone_jobs[job_id]["html"] = generated_code.get("html")
    except Exception as e:
        clone_jobs[job_id]["status"] = "failed"
        clone_jobs[job_id]["progress"] = 100
        clone_jobs[job_id]["message"] = f"Error: {str(e)}"
        clone_jobs[job_id]["error"] = str(e)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)