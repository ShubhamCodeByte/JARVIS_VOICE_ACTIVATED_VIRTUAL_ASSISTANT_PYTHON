# Jarvis — Voice-Activated Virtual Assistant

Jarvis is a voice-activated virtual assistant that listens for your commands and performs tasks like web browsing, music playback, fetching jokes, and answering complex queries — powered by gemini-3.1-flash-lite-preview

## Features

- **Wake Word Detection** — Activates on the keyword "Jarvis"
- **Voice Recognition** — Uses speech_recognition to interpret spoken commands
- **Text-to-Speech** — Responds via pyttsx3 or gTTS + pygame
- **Web Browsing** — Opens Google, YouTube, Facebook, LinkedIn on command
- **Music Playback** — Plays songs via web links through a musicLibrary module
- **AI Responses** — Handles open-ended queries using gemini-3.1-flash-lite-preview

## Installation

```bash
git clone https://github.com/ShubhamCodeByte/JARVIS_VOICE_ACTIVATED_VIRTUAL_ASSISTANT_PYTHON.git
cd jarvis
pip install -r Requirements.txt
```

Set up a `.env` file:

```
OPENAI_API_KEY=your_gemini_api_key
```

Then run:

```bash
python jarvis.py
```
