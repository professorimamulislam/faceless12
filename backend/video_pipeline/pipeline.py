"""
Local video generation pipeline.

- Tries to use Diffusers + torch if available and a local model path is present.
- Otherwise, falls back to generating synthetic images with overlaid text.
- Builds a simple multi-scene video using MoviePy, with gentle zoom and crossfades.
- Optional background music (procedural) and TTS if Coqui TTS is installed.

This module is designed to run fully offline (no external API). For true AI image
synthesis, ensure you have a local Diffusers model available and accessible.
Set the environment variable DIFFUSERS_MODEL_PATH to point to it, or place it under
"backend/models/stable-diffusion". If no model is found, a placeholder pipeline is used.
"""
from __future__ import annotations

import os
import math
import logging
from pathlib import Path
from typing import Dict, List, Optional

from PIL import Image, ImageDraw, ImageFont
import numpy as np

from moviepy.editor import (
    ImageClip,
    concatenate_videoclips,
    CompositeAudioClip,
)
from moviepy.video.fx import all as vfx

from . import audio as audio_utils
from . import tts as tts_utils

logger = logging.getLogger("video_pipeline")

# Optional Diffusers support
try:
    import torch  # type: ignore
    from diffusers import StableDiffusionPipeline  # type: ignore

    DIFFUSERS_AVAILABLE = True
except Exception:  # pragma: no cover
    DIFFUSERS_AVAILABLE = False
    torch = None
    StableDiffusionPipeline = None  # type: ignore


STYLE_PRESETS = {
    "cinematic": {
        "add": "cinematic, moody lighting, high detail, 4k, shallow depth of field",
        "neg": "text, watermark, logo, signature, face, person, human, hands",
    },
    "anime": {
        "add": "anime style, clean lines, cel shading, vibrant colors",
        "neg": "realistic face, text, watermark, logo, signature, photorealistic",
    },
    "neon": {
        "add": "neon glow, cyberpunk, high contrast, vibrant lights",
        "neg": "face, watermark, text, logo, blurry",
    },
    "watercolor": {
        "add": "watercolor painting, soft brush strokes, pastel tones",
        "neg": "face, text, watermark, logo, photorealistic",
    },
    "photoreal": {
        "add": "photorealistic, high detail, 50mm lens, volumetric light",
        "neg": "face, person, text, watermark, logo, deformed",
    },
}


def _load_sd_pipeline(model_path: Optional[str]) -> Optional["StableDiffusionPipeline"]:
    if not DIFFUSERS_AVAILABLE:
        return None

    path = None
    if model_path and Path(model_path).exists():
        path = model_path
    else:
        fallback = Path(__file__).resolve().parents[1] / "models" / "stable-diffusion"
        if fallback.exists():
            path = str(fallback)

    if not path:
        logger.warning("No local Diffusers model found. Using placeholder pipeline.")
        return None

    try:
        logger.info(f"Loading Diffusers model from {path} (local_files_only=True)")
        pipe = StableDiffusionPipeline.from_pretrained(path, local_files_only=True)
        device = "cuda" if torch and torch.cuda.is_available() else "cpu"
        pipe = pipe.to(device)
        pipe.safety_checker = None  # avoid NSFW filter interfering with faceless scenes
        return pipe
    except Exception as e:  # pragma: no cover
        logger.error(f"Failed to load Diffusers model: {e}")
        return None


def split_prompt_into_scenes(prompt: str, num_scenes: int) -> List[str]:
    # Split by sentence terminators first, then pad/truncate to desired length
    raw = [s.strip() for s in
           prompt.replace("?", ".").replace("!", ".").split(".") if s.strip()]
    if not raw:
        raw = [prompt.strip()]

    if len(raw) >= num_scenes:
        return raw[:num_scenes]

    # If fewer sentences than scenes, evenly duplicate/extend
    out = []
    i = 0
    while len(out) < num_scenes:
        out.append(raw[i % len(raw)])
        i += 1
    return out


def _placeholder_image(text: str, size=(1280, 720)) -> Image.Image:
    # Generate a gradient background with text overlay
    w, h = size
    rng = np.random.default_rng(abs(hash(text)) % (2**32))
    c1 = np.array(rng.integers(0, 255, size=3))
    c2 = np.array(rng.integers(0, 255, size=3))
    grad = np.linspace(0, 1, w)
    row = (c1[None, :] * (1 - grad[:, None]) + c2[None, :] * grad[:, None]).astype(np.uint8)
    img = np.repeat(row[None, :, :], h, axis=0)
    image = Image.fromarray(img, mode="RGB")

    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except Exception:
        font = ImageFont.load_default()

    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    text_wrap = f"{text[:80]}" + ("..." if len(text) > 80 else "")
    bbox = odraw.textbbox((0, 0), text_wrap, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    pad = 20
    box_w, box_h = tw + pad * 2, th + pad * 2
    x, y = (w - box_w) // 2, h - box_h - 40
    odraw.rectangle([x, y, x + box_w, y + box_h], fill=(0, 0, 0, 128))
    odraw.text((x + pad, y + pad), text_wrap, font=font, fill=(255, 255, 255, 255))

    image = Image.alpha_composite(image.convert("RGBA"), overlay)
    return image.convert("RGB")


def _generate_image(scene_prompt: str, style: str, seed: Optional[int], pipe) -> Image.Image:
    if pipe is None:
        return _placeholder_image(scene_prompt)

    preset = STYLE_PRESETS.get(style, STYLE_PRESETS["cinematic"])  # default
    full_prompt = f"{scene_prompt}, {preset['add']}"
    negative = preset["neg"]

    try:
        generator = None
        if seed is not None and torch is not None:
            device = pipe.device
            generator = torch.Generator(device=device).manual_seed(int(seed))
        result = pipe(
            prompt=full_prompt,
            negative_prompt=negative,
            guidance_scale=7.0,
            num_inference_steps=30,
            width=768,
            height=432,
            generator=generator,
        )
        image = result.images[0]
        return image
    except Exception as e:  # pragma: no cover
        logger.error(f"Diffusers generation failed, using placeholder. Error: {e}")
        return _placeholder_image(scene_prompt)


def _make_scene_clip(img_path: str, duration: float) -> ImageClip:
    clip = ImageClip(img_path).set_duration(duration)
    # Gentle zoom-in over the scene duration
    def scale_at(t):
        return 1.0 + 0.06 * (t / max(duration, 1e-6))

    clip = clip.fx(vfx.resize, scale_at).set_position("center")
    return clip


def generate_video_job(job_id: str, params: Dict, jobs: Dict, media_dirs: Dict[str, str]):
    """
    Background task entrypoint. Updates jobs[job_id] inplace.
    """
    job = jobs[job_id]
    job.status = "running"
    job.message = "Initializing"
    job.progress = 2.0

    base_dir = Path(media_dirs["base"]) if "base" in media_dirs else Path(__file__).resolve().parents[1] / "media"
    videos_dir = Path(media_dirs.get("videos", base_dir / "videos"))
    frames_dir = Path(media_dirs.get("frames", base_dir / "frames"))
    audio_dir = Path(media_dirs.get("audio", base_dir / "audio"))

    for d in (videos_dir, frames_dir, audio_dir):
        d.mkdir(parents=True, exist_ok=True)

    prompt: str = params.get("prompt", "").strip()
    style: str = params.get("style", "cinematic")
    num_scenes: int = int(params.get("num_scenes", 5))
    duration: float = float(params.get("duration_per_scene", 3.0))
    fps: int = int(params.get("fps", 24))
    add_music: bool = bool(params.get("add_music", True))
    add_tts: bool = bool(params.get("add_tts", False))
    voice: Optional[str] = params.get("voice")
    seed: Optional[int] = params.get("seed")

    # Load pipeline if available
    model_path = os.getenv("DIFFUSERS_MODEL_PATH")
    pipe = _load_sd_pipeline(model_path)

    # Prepare scenes
    scenes = split_prompt_into_scenes(prompt, num_scenes)
    total_steps = num_scenes + 3  # images + assembling + audio + writing
    progress_per = max(100.0 / max(total_steps, 1), 1.0)

    frame_paths: List[str] = []
    try:
        # Generate scene images
        for i, s in enumerate(scenes):
            job.message = f"Generating scene {i+1}/{num_scenes}"
            job.progress = min(95.0, 5.0 + (i + 1) * progress_per)

            img = _generate_image(s, style=style, seed=(None if seed is None else seed + i), pipe=pipe)
            frame_path = frames_dir / f"{job_id}_scene_{i+1:02d}.png"
            img.save(frame_path)
            frame_paths.append(str(frame_path))

        job.message = "Assembling video"
        job.progress = min(98.0, job.progress + progress_per)

        # Build video clips with crossfades
        crossfade = min(0.6, duration * 0.2)
        clips = []
        for idx, fp in enumerate(frame_paths):
            c = _make_scene_clip(fp, duration)
            if idx > 0 and crossfade > 0:
                c = c.crossfadein(crossfade)
            clips.append(c)

        video = concatenate_videoclips(clips, method="compose", padding=(-crossfade if crossfade > 0 else 0))

        # Optional audio
        audio_clips = []
        total_duration = max(0.1, num_scenes * duration - max(0.0, (num_scenes - 1) * crossfade))

        if add_tts:
            job.message = "Synthesizing voiceover"
            tts_path = audio_utils.safe_join(audio_dir, f"{job_id}_tts.wav")
            tts_generated = tts_utils.synthesize_tts(text=". ".join(scenes), out_path=str(tts_path), voice=voice)
            if tts_generated:
                try:
                    from moviepy.editor import AudioFileClip
                    audio_clips.append(AudioFileClip(tts_generated))
                except Exception as e:  # pragma: no cover
                    logger.warning(f"Failed loading TTS audio clip: {e}")

        if add_music:
            job.message = "Generating background music"
            music_clip = audio_utils.background_music_clip(duration=total_duration)
            if music_clip:
                # lower volume for background
                audio_clips.append(music_clip.volumex(0.2))

        if audio_clips:
            video = video.set_audio(CompositeAudioClip(audio_clips))

        # Write final video
        job.message = "Writing video"
        out_path = videos_dir / f"{job_id}.mp4"
        video.write_videofile(
            str(out_path),
            fps=fps,
            codec="libx264",
            audio_codec="aac",
            preset="medium",
            threads=os.cpu_count() or 4,
            verbose=False,
            logger=None,
        )

        # Update job and cleanup
        rel = f"/media/videos/{out_path.name}"
        job.status = "completed"
        job.progress = 100.0
        job.message = "Done"
        job.video_url = rel

    except Exception as e:  # pragma: no cover
        logger.exception("Video generation failed")
        job.status = "failed"
        job.message = str(e)
        job.progress = 100.0


# Utilities in audio.py and tts.py
