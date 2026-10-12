# VisionSpeak: Zero-API / Offline Operation Manual

## 1. Core Principle
VisionSpeak does not require, accept, or rely on paid third-party AI APIs (such as OpenAI, Anthropic, or Google Gemini).
All image captioning operates locally on your machine.

## 2. Model Architecture
- **Vision Model**: Salesforce BLIP (`Salesforce/blip-image-captioning-base`).
- **Inference Hardware**: PyTorch CPU or CUDA (if NVIDIA GPU is detected).
- **Weight Cache**: Model weights are stored outside the workspace in `~/.cache/huggingface/hub/` to keep the project folder size strictly under 500 MB.

## 3. Fallback Engine
When running in ultra-constrained environments without PyTorch or during initial setup, VisionSpeak includes a deterministic linguistic rule engine that provides instant suggestions based on file fingerprints and user tone selections without throwing network errors.
