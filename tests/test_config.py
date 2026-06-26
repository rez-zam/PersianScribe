"""Unit tests for the TranscriptionConfig schema."""

from __future__ import annotations

from pathlib import Path

import pytest

from persianscribe.config import TranscriptionConfig


def test_defaults() -> None:
    """Default configuration should target the Persian medium model."""
    config = TranscriptionConfig()
    assert config.model_size == "medium"
    assert config.language == "fa"
    assert config.task == "transcribe"
    assert config.output_dir == Path("./outputs")


def test_str_output_dir_is_coerced_to_path() -> None:
    """A string output_dir should be normalized to a Path instance."""
    config = TranscriptionConfig(output_dir=Path("custom"))
    assert isinstance(config.output_dir, Path)


@pytest.mark.parametrize("bad_model", ["huge", "x-large", ""])
def test_invalid_model_size_raises(bad_model: str) -> None:
    """Unsupported model sizes should raise ValueError."""
    with pytest.raises(ValueError, match="Invalid model_size"):
        TranscriptionConfig(model_size=bad_model)


def test_invalid_device_raises() -> None:
    """Unsupported device preferences should raise ValueError."""
    with pytest.raises(ValueError, match="Invalid device_preference"):
        TranscriptionConfig(device_preference="gpu")


def test_invalid_task_raises() -> None:
    """Unsupported tasks should raise ValueError."""
    with pytest.raises(ValueError, match="Invalid task"):
        TranscriptionConfig(task="summarize")