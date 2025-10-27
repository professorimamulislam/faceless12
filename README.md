# Faceless AI Video (Fullstack)

Production-ready local web app to generate faceless AI videos from prompts.

## Stack
- Frontend: Next.js 14 + TailwindCSS
- Backend: FastAPI (Python)
- Video: MoviePy/FFmpeg
- Optional: Diffusers (Stable Diffusion), Coqui TTS

## Structure
```
faceless-ai-video/
  backend/
    app.py
    requirements.txt
    video_pipeline/
      pipeline.py
      audio.py
      tts.py
  frontend/
    package.json
    app/
      layout.js, page.js, ...
    components/
    lib/
    tailwind.config.js
    postcss.config.js
    next.config.js
```

## Prereqs
- Node.js 18+
- Python 3.10+

## Run (Windows PowerShell)
1) Backend
```
cd backend
python -m venv .venv
.venv/Scripts/Activate.ps1
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

2) Frontend (in a new terminal)
```
cd frontend
npm install
npm run dev
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000

Optional: set `NEXT_PUBLIC_API_BASE` to point the frontend at a non-default backend URL.

## Notes
- First run may download a local FFmpeg binary via imageio-ffmpeg; it remains cached.
- For real image generation, install `torch` + `diffusers` and place a local model under `backend/models/stable-diffusion` or set `DIFFUSERS_MODEL_PATH`.
- For TTS, install `TTS` python package.
