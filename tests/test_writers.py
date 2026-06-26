"""Unit tests for the output writers."""

from __future__ import annotations

from pathlib import Path

import pytest

from persianscribe.writers import format_timestamp, write_srt, write_txt

# Minimal segment fixtures mimicking Whisper's output schema.
SAMPLE_SEGMENTS = [
    {"start": 0.0, "end": 2.5, "text": " سلام دنیا "},
    {"start": 2.5, "end": 5.0, "text": " این یک تست است "},
]


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0.0, "00:00:00,000"),
        (1.5, "00:00:01,500"),
        (83.456, "00:01:23,456"),
        (3661.0, "01:01:01,000"),
    ],
)
def test_format_timestamp(seconds: float, expected: str) -> None:
    """Timestamps should be formatted as HH:MM:SS,mmm."""
    assert format_timestamp(seconds) == expected


def test_write_txt(tmp_path: Path) -> None:
    """TXT output should contain one stripped line per segment."""
    txt_path = tmp_path / "out.txt"
    write_txt(SAMPLE_SEGMENTS, txt_path)

    lines = txt_path.read_text(encoding="utf-8").splitlines()
    assert lines == ["سلام دنیا", "این یک تست است"]


def test_write_srt(tmp_path: Path) -> None:
    """SRT output should contain numbered, timestamped blocks."""
    srt_path = tmp_path / "out.srt"
    write_srt(SAMPLE_SEGMENTS, srt_path)

    content = srt_path.read_text(encoding="utf-8")
    assert "1\n00:00:00,000 --> 00:00:02,500\nسلام دنیا" in content
    assert "2\n00:00:02,500 --> 00:00:05,000\nاین یک تست است" in content


def test_write_creates_parent_dirs(tmp_path: Path) -> None:
    """Writers should create missing parent directories automatically."""
    nested = tmp_path / "a" / "b" / "out.txt"
    write_txt(SAMPLE_SEGMENTS, nested)
    assert nested.exists()