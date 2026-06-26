"""Minimal end-to-end example of using the PersianScribe Python API."""

from __future__ import annotations

from pathlib import Path

from persianscribe import TranscriptionConfig, WhisperTranscriber


def main() -> None:
    """Transcribe a single audio file and print a short preview."""
    config = TranscriptionConfig(
        model_size="small",       # Lighter model for a quick demo.
        device_preference="auto",
        language="fa",
        make_docx=True,
        output_dir=Path("./outputs"),
    )

    transcriber = WhisperTranscriber(config)
    transcriber.load()

    audio_path = Path("examples/sample.m4a")  # Replace with your own file.
    result = transcriber.transcribe(audio_path)

    print(f"TXT : {result.txt_path}")
    print(f"SRT : {result.srt_path}")
    if result.docx_path:
        print(f"DOCX: {result.docx_path}")

    preview = "".join(seg.get("text", "") for seg in result.segments)[:500]
    print("\n--- Preview ---\n", preview)


if __name__ == "__main__":
    main()