"""Configuration schema and shared constants for PersianScribe."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

# Audio/video container extensions accepted by the pipeline.
SUPPORTED_EXTENSIONS: frozenset[str] = frozenset(
    {".m4a", ".mp3", ".wav", ".flac", ".mkv", ".mp4", ".aac", ".ogg", ".wma", ".m4b"}
)

# Valid Whisper checkpoint sizes (in increasing order of accuracy/cost).
VALID_MODEL_SIZES: frozenset[str] = frozenset(
    {"tiny", "base", "small", "medium", "large"}
)


@dataclass(slots=True)
class TranscriptionConfig:
    """User-facing configuration for a transcription run.

    Attributes:
        model_size:        Whisper checkpoint size: tiny | base | small | medium | large.
        device_preference: Compute device preference: auto | cuda | cpu.
        language:          ISO-639 language code of the audio (e.g. "fa" for Persian).
        task:              "transcribe" (same language) or "translate" (to English).
        make_docx:         Whether to additionally export a formatted DOCX file.
        output_dir:        Directory where TXT/SRT/DOCX outputs are written.
    """

    model_size: str = "medium"
    device_preference: str = "auto"
    language: str = "fa"
    task: str = "transcribe"
    make_docx: bool = False
    output_dir: Path = field(default_factory=lambda: Path("./outputs"))

    def __post_init__(self) -> None:
        """Validate field values and normalize the output directory."""
        if self.model_size not in VALID_MODEL_SIZES:
            raise ValueError(
                f"Invalid model_size '{self.model_size}'. "
                f"Expected one of: {sorted(VALID_MODEL_SIZES)}"
            )
        if self.device_preference not in {"auto", "cuda", "cpu"}:
            raise ValueError(
                f"Invalid device_preference '{self.device_preference}'. "
                "Expected one of: auto, cuda, cpu"
            )
        if self.task not in {"transcribe", "translate"}:
            raise ValueError(
                f"Invalid task '{self.task}'. Expected 'transcribe' or 'translate'."
            )
        # Ensure output_dir is always a Path instance (allows passing str).
        self.output_dir = Path(self.output_dir)