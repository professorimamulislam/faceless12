"""
FastAPI backend for local faceless AI video generation from prompts.
Endpoints:
- POST /api/generate-video -> start a background job to generate a video from a prompt
- GET  /api/status/{job_id} -> query job status and (when complete) get video URL
- Static /media -> serves generated videos and temp assets

Video generation pipeline is implemented in video_pipeline/pipeline.py
It uses local models if available (Diffusers + torch) and falls back to a placeholder
synthetic image pipeline when models are not installed. MoviePy/FFmpeg is used
for video compilation.
"""
from __future__ import annotations

import os
import uuid
import logging
from pathlib import Path
from typing import Dict, Optional

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from video_pipeline.pipeline import generate_video_job, DIFFUSERS_AVAILABLE


BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / "media"
VIDEOS_DIR = MEDIA_DIR / "videos"
FRAMES_DIR = MEDIA_DIR / "frames"
AUDIO_DIR = MEDIA_DIR / "audio"

for d in (MEDIA_DIR, VIDEOS_DIR, FRAMES_DIR, AUDIO_DIR):
    d.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("video_api")
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

app = FastAPI(title="Faceless AI Video API", version="1.0.0")

# CORS for local dev frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated media
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")


class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="Text prompt describing the video")
    num_scenes: int = Field(5, ge=1, le=10, description="Number of scenes to split prompt into")
    style: str = Field("cinematic", description="Style preset: cinematic|anime|neon|watercolor|photoreal")
    duration_per_scene: float = Field(3.0, gt=0, le=15)
    fps: int = Field(24, ge=8, le=60)
    add_music: bool = Field(True)
    add_tts: bool = Field(False)
    voice: Optional[str] = Field("en", description="TTS voice/language hint")
    seed: Optional[int] = Field(None)


class JobStatus(BaseModel):
    job_id: str
    status: str  # pending|running|completed|failed
    progress: float
    message: Optional[str] = None
    video_url: Optional[str] = None


# Simple in-memory job registry
JOBS: Dict[str, JobStatus] = {}


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "media_dir": str(MEDIA_DIR),
        "diffusers_available": bool(DIFFUSERS_AVAILABLE),
    }


@app.post("/api/generate-video", response_model=JobStatus)
async def generate_video(payload: GenerateRequest, background_tasks: BackgroundTasks):
    prompt = payload.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    job_id = uuid.uuid4().hex
    job = JobStatus(job_id=job_id, status="pending", progress=0.0, message="Queued", video_url=None)
    JOBS[job_id] = job

    # Schedule background processing
    background_tasks.add_task(
        generate_video_job,
        job_id=job_id,
        params=payload.model_dump(),
        jobs=JOBS,
        media_dirs={
            "base": str(MEDIA_DIR),
            "videos": str(VIDEOS_DIR),
            "frames": str(FRAMES_DIR),
            "audio": str(AUDIO_DIR),
        },
    )

    return job


@app.get("/api/status/{job_id}", response_model=JobStatus)
async def get_status(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # If completed, ensure URL is kept relative to /media mount
    if job.status == "completed" and job.video_url:
        # Normalize backslashes for Windows
        job.video_url = job.video_url.replace("\\", "/")

    return job


if __name__ == "__main__":
    # For local manual run: python app.py
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
