# VisionSpeak AI 📸✨

> **Local, 100% Offline AI Image Captioning Platform with Zero API Keys and Zero Cloud Fees.**

VisionSpeak AI generates grounded, creative, aesthetic, and emotional captions for images directly on your local machine using **Salesforce BLIP** with PyTorch CPU/CUDA, accompanied by a fast deterministic fallback engine.

---

## 🌟 Key Features

- **100% Offline & Free**: No OpenAI, Anthropic, or external API keys needed.
- **Genuine AI Vision**: Uses local Salesforce BLIP (`Salesforce/blip-image-captioning-base`).
- **3 Caption Styles**: Aesthetic, Emotional, and Creative / Trending with curated hashtags.
- **Text-to-Speech (TTS)**: Listen to captions using Web Speech Synthesis.
- **SQLite History**: Persistent local generation history and audit log.
- **Exporting**: Instant export to JSON, CSV, and plain text.
- **Modern Glassmorphic UI**: React 18, Vite, and dark/light navy themes.

---

## 📁 Architecture Overview

```
VISIONSPEAK/
├── visionspeak/              # Python Local AI Core
│   ├── models/blip.py        # Salesforce BLIP model engine
│   ├── processing/           # PIL image validation & preprocessing
│   ├── generation/           # Multi-style caption orchestrator
│   ├── storage/              # SQLite database & repository
│   ├── api/app.py            # FastAPI REST backend
│   └── cli.py                # Command-line interface
├── backend/                  # Node.js Express Gateway
├── frontend/                 # Vite + React + Tailwind UI
├── tests/                    # Pytest unit & integration test suite
└── scripts/                  # LOC counter, PR engine, benchmarks
```

---

## 🚀 Quick Start (Windows)

### Prerequisites
- Python 3.10+
- Node.js 18+

### Setup & Run
```powershell
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Run unit tests
pytest tests/unit -v

# 3. Start Python API backend
python -m visionspeak.api.app

# 4. In a second terminal, start React frontend
cd frontend
npm install
npm run dev
```
