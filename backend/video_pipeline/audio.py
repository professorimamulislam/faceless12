"""
Audio utilities: procedural background music and helpers.
"""
from __future__ import annotations

import os
import numpy as np
from typing import Optional

from moviepy.audio.AudioClip import AudioArrayClip


def background_music_clip(duration: float, sr: int = 44100) -> Optional[AudioArrayClip]:
    """
    Generate a simple procedural ambient background track as an AudioArrayClip.
    This avoids external assets and keeps everything local.
    """
    try:
        duration = float(max(0.1, duration))
        t = np.linspace(0, duration, int(sr * duration), endpoint=False)
        # Two gentle sine waves + soft noise
        base = 0.03 * np.sin(2 * np.pi * 220 * t)
        pad = 0.02 * np.sin(2 * np.pi * 440 * t + np.pi / 3)
        noise = 0.005 * np.random.default_rng(0).normal(size=t.shape)
        y = (base + pad + noise).astype(np.float32)
        stereo = np.stack([y, y], axis=1)
        return AudioArrayClip(stereo, fps=sr)
    except Exception:
        return None


def safe_join(folder, filename):
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, filename)
