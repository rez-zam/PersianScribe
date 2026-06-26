"""High-level Whisper model wrapper and transcription orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import torch
import whisper

from .config import TranscriptionConfig
from .writers import write_docx, write_srt, write_txt


@dataclass
class TranscriptionResult:
    """Bundles the artifacts produced for a single audio file.

    Attributes:
        txt_path:  Path to the generated plain-text transcript.
        srt_path:  Path to the generated SRT subtitle file.
        docx_path: Path to the generated DOCX file, or None if not requested.
        segments:  Raw Whisper segments for downstream processing/preview.
    """

    txt_path: Path
    srt_path: Path
    docx_path: Optional[Path]
    segments: list[dict[str, Any]]


class WhisperTranscriber:
    """High-level wrapper around an OpenAI Whisper model.

    Handles device resolution, lazy model loading, and per-file transcription
    with automatic export to TXT/SRT (and optionally DOCX).
    """

    def __init__(self, config: TranscriptionConfig) -> None:
        self.config = config
        self.device, self.use_fp16 = self._resolve_device(config.device_preference)
        self._model: Optional[whisper.Whisper] = None

    @staticmethod
    def _resolve_device(preference: str) -> tuple[str, bool]:
        """Resolve the effective device and whether FP16 inference is enabled.

        FP16 is only enabled on CUDA devices, as CPU FP16 is unsupported by Whisper.

        Args:
            preference: One of "auto", "cuda", or "cpu".

        Returns:
            A tuple of (device, use_fp16).
        """
        cuda_available = torch.cuda.is_available()
        if preference == "cpu":
            return "cpu", False
        if preference == "cuda" and not cuda_available:
            print("⚠️  CUDA requested but unavailable — falling back to CPU.")
        device = "cuda" if (preference != "cpu" and cuda_available) else "cpu"
        return device, device == "cuda"

    def load(self) -> None:
        """Load the Whisper checkpoint onto the resolved device (idempotent)."""
        if self._model is not None:
            return
        print(
            f"Loading Whisper model '{self.config.model_size}' "
            f"on {self.device} (fp16={self.use_fp16}) ..."
        )
        self._model = whisper.load_model(self.config.model_size, device=self.device)
        print("Model loaded successfully.")

    @property
    def model(self) -> whisper.Whisper:
        """Return the loaded model, loading it on first access if needed."""
        if self._model is None:
            self.load()
        assert self._model is not None
        return self._model

    def transcribe(self, audio_path: Path) -> TranscriptionResult:
        """Transcribe a single audio file and persist its outputs.

        Args:
            audio_path: Path to the source audio/video file.

        Returns:
            A TranscriptionResult describing every generated artifact.
        """
        result = self.model.transcribe(
            str(audio_path),
            language=self.config.language,
            task=self.config.task,
            verbose=False,
            fp16=self.use_fp16,
        )
        segments: list[dict[str, Any]] = result.get("segments", [])

        stem = audio_path.stem
        txt_path = self.config.output_dir / f"{stem}.txt"
        srt_path = self.config.output_dir / f"{stem}.srt"
        write_txt(segments, txt_path)
        write_srt(segments, srt_path)

        docx_path: Optional[Path] = None
        if self.config.make_docx:
            docx_path = self.config.output_dir / f"{stem}.docx"
            write_docx(segments, docx_path, include_timestamps=True)

        return TranscriptionResult(txt_path, srt_path, docx_path, segments)