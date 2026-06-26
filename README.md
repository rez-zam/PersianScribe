<div align="center">

# 🇮🇷 PersianScribe

**A Whisper-powered Persian audio-to-text toolkit**

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

PersianScribe converts audio/video files into text using OpenAI Whisper,
producing **TXT**, **SRT**, and optional **DOCX** outputs. It runs on both
**GPU (CUDA)** and **CPU**, and supports single-file, batch, and notebook modes.

## ✨ Features

- 🎯 Optimized for **Persian (fa)** transcription
- ⚡ Automatic **GPU/CPU** detection with FP16 acceleration
- 📦 Multiple modes: single file · batch folder · Jupyter widget
- 📄 Exports to **TXT / SRT / DOCX**
- 🌐 Optional **translation** to English

## 🚀 Installation

```bash
git clone https://github.com/rez-zam/PersianScribe.git
cd PersianScribe
pip install -e .
```

> **Note:** `ffmpeg` must be installed and available on your PATH.
> - **Ubuntu/Debian:** `sudo apt-get install ffmpeg`
> - **Windows:** download from [ffmpeg.org](https://ffmpeg.org) and add to PATH

## 📖 Usage

### Command Line
```bash
persianscribe transcribe "audio.m4a" --model medium --language fa
persianscribe batch "./audio_folder" --output ./outputs --docx
```

### Python API
```python
from persianscribe import TranscriptionConfig, WhisperTranscriber
from pathlib import Path

config = TranscriptionConfig(model_size="medium", language="fa")
transcriber = WhisperTranscriber(config)
result = transcriber.transcribe(Path("audio.m4a"))
print(result.txt_path)
```

## 🤝 Contributing
Pull requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## 📜 License
Distributed under the MIT License. See [LICENSE](LICENSE).