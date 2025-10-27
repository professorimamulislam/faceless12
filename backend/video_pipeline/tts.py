"""
Optional Coqui TTS integration. If the TTS package is not installed, functions
silently no-op and return None.
"""
from __future__ import annotations

from typing import Optional


def synthesize_tts(text: str, out_path: str, voice: Optional[str] = None) -> Optional[str]:
    try:
        # Lazy import; library is heavy and optional
        from TTS.api import TTS  # type: ignore
    except Exception:
        return None

    try:
        # Select a simple multilingual model if available; adjust per local install
        # Example: "tts_models/en/ljspeech/tacotron2-DDC"
        model_name = "tts_models/en/ljspeech/tacotron2-DDC"
        tts = TTS(model_name)
        tts.tts_to_file(text=text, file_path=out_path)
        return out_path
    except Exception:
        return None
