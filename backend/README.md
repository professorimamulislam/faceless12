# Faceless AI Video Backend (FastAPI)

Local-only API that generates short, faceless videos from a text prompt. Uses MoviePy/FFmpeg to assemble a multi-scene video. For true image synthesis, plug in a local Diffusers model; otherwise a high-quality placeholder generator is used.

## Endpoints
- POST `/api/generate-video` → starts a background job; returns `{ job_id, status, progress }`
- GET `/api/status/{job_id}` → returns job status `{ status, progress, message, video_url }`
- Static media is served under `/media` (e.g. `/media/videos/<id>.mp4`)

## Quickstart
1. Python 3.10+
2. Create venv and install deps
   ```bash
   python -m venv .venv
   .venv/Scripts/activate  # Windows PowerShell
   pip install -r requirements.txt
   ```
3. Run API
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

Open http://localhost:8000/api/health to verify.

## Optional: Real AI image generation (Diffusers)
- Install torch + diffusers compatible with your CPU/GPU.
- Place a local model under `backend/models/stable-diffusion/` OR set env var `DIFFUSERS_MODEL_PATH` to a local model path.
- The server does not download any models; ensure weights are present locally.

## Optional: Text-to-Speech (Coqui TTS)
- Install `TTS` package and its dependencies.
- The pipeline will automatically use it if available to synthesize a simple voiceover.

## Output
- Videos are written to `backend/media/videos/<job_id>.mp4`.
- Temporary frames to `backend/media/frames/` and audio (if any) to `backend/media/audio/`.

## Notes
- All processing is local. No external API calls are used.
- MoviePy leverages FFmpeg via `imageio-ffmpeg`, which will download a Windows binary on first run; once cached locally, it stays offline.
