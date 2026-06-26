"""Command-line interface for PersianScribe."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import SUPPORTED_EXTENSIONS, TranscriptionConfig
from .transcriber import WhisperTranscriber


def _build_parser() -> argparse.ArgumentParser:
    """Construct the top-level argument parser with sub-commands."""
    parser = argparse.ArgumentParser(
        prog="persianscribe",
        description="Transcribe Persian audio to text using OpenAI Whisper.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Shared options reused across sub-commands.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--model", default="medium", help="Whisper model size.")
    common.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    common.add_argument("--language", default="fa", help="ISO-639 language code.")
    common.add_argument(
        "--task", default="transcribe", choices=["transcribe", "translate"]
    )
    common.add_argument("--output", default="./outputs", help="Output directory.")
    common.add_argument("--docx", action="store_true", help="Also export DOCX.")

    transcribe_cmd = subparsers.add_parser(
        "transcribe", parents=[common], help="Transcribe a single file."
    )
    transcribe_cmd.add_argument("path", help="Path to the audio/video file.")

    batch_cmd = subparsers.add_parser(
        "batch", parents=[common], help="Transcribe a folder recursively."
    )
    batch_cmd.add_argument("path", help="Path to the input folder.")

    return parser


def _make_config(args: argparse.Namespace) -> TranscriptionConfig:
    """Translate parsed CLI arguments into a TranscriptionConfig."""
    return TranscriptionConfig(
        model_size=args.model,
        device_preference=args.device,
        language=args.language,
        task=args.task,
        make_docx=args.docx,
        output_dir=Path(args.output),
    )


def main() -> None:
    """Entry point invoked by the `persianscribe` console script."""
    parser = _build_parser()
    args = parser.parse_args()

    transcriber = WhisperTranscriber(_make_config(args))
    transcriber.load()

    target = Path(args.path)

    if args.command == "transcribe":
        if not target.exists():
            raise FileNotFoundError(f"File not found: {target}")
        result = transcriber.transcribe(target)
        print(f"Saved: {result.txt_path} | {result.srt_path}")
        if result.docx_path:
            print(f"       {result.docx_path}")

    elif args.command == "batch":
        if not target.exists():
            raise FileNotFoundError(f"Folder not found: {target}")
        files = sorted(
            p for p in target.rglob("*") if p.suffix.lower() in SUPPORTED_EXTENSIONS
        )
        print(f"Found {len(files)} file(s).")
        for path in files:
            try:
                transcriber.transcribe(path)
                print(f"  ✓ {path.name}")
            except Exception as exc:  # noqa: BLE001 — keep the batch alive on errors
                print(f"  ✗ {path.name}: {exc}")
        print(f"Done. Outputs are in: {transcriber.config.output_dir.resolve()}")


if __name__ == "__main__":
    main()