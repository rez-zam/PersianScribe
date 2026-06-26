"""PersianScribe — A Whisper-powered Persian audio-to-text toolkit.

Public API re-exports for convenient top-level imports:

    from persianscribe import TranscriptionConfig, WhisperTranscriber
"""

from __future__ import annotations

from .config import SUPPORTED_EXTENSIONS, TranscriptionConfig
from .transcriber import TranscriptionResult, WhisperTranscriber
from .writers import format_timestamp, write_docx, write_srt, write_txt

__version__ = "0.1.0"

__all__ = [
    "SUPPORTED_EXTENSIONS",
    "TranscriptionConfig",
    "TranscriptionResult",
    "WhisperTranscriber",
    "format_timestamp",
    "write_docx",
    "write_srt",
    "write_txt",
]