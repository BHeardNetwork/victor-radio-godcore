#!/usr/bin/env python3
"""
VICTOR RADIO CORE v1.0.0-GODCORE
Self-running AI radio brain.
Integrates VictorCore memory, local LLM (Ollama), VictorVoice, playlist management.
Uncle Grok | Bando Empire | Financial Freedom Engine
"""

import os
import time
import json
import threading
import subprocess
import random
from datetime import datetime
from pathlib import Path

# === CONFIG ===
RADIO_ROOT = Path(__file__).parent.parent
AUDIO_DIR = RADIO_ROOT / "audio_segments"
MUSIC_DIR = RADIO_ROOT / "music"  # Put your royalty-free MP3s here
PLAYLIST_FILE = RADIO_ROOT / "current_playlist.m3u"
STATE_FILE = RADIO_ROOT / "state" / "radio_state.json"
LOG_FILE = RADIO_ROOT / "logs" / "victor_radio.log"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
(RADIO_ROOT / "state").mkdir(exist_ok=True)
(RADIO_ROOT / "logs").mkdir(exist_ok=True)

# Ollama config (user must have Ollama running with a model, e.g. llama3 or qwen)
OLLAMA_MODEL = "llama3"  # or your preferred local model
OLLAMA_URL = "http://localhost:11434/api/generate"

# Victor Voice stub (extend with your full VictorVoice / synth.py)
def synthesize_victor_voice(text: str, output_path: Path) -> bool:
    """Stub - replace with your full VictorVoice / synth.py logic"""
    try:
        # Simple fallback using pyttsx3 if available
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.save_to_file(text, str(output_path))
        engine.runAndWait()
        return True
    except Exception as e:
        print(f"[VOICE] Fallback failed: {e}. Using placeholder.")
        # Placeholder: create silent or simple tone
        with open(output_path, "wb") as f:
            f.write(b"")  # TODO: replace with real synthesis
        return False

def call_ollama(prompt: str) -> str:
    """Call local Ollama for show script generation"""
    try:
        import requests
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.85, "top_p": 0.9}
        }
        resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
        if resp.status_code == 200:
            return resp.json().get("response", "").strip()
        return "The empire continues to evolve in silence tonight."
    except Exception as e:
        print(f"[LLM] Ollama error: {e}")
        return "Financial freedom is built one autonomous broadcast at a time."

class VictorRadioCore:
    def __init__(self):
        self.state = self._load_state()
        self.playlist = []
        self.is_running = False
        self.generation_thread = None

    def _load_state(self):
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                return json.load(f)
        return {
            "last_show": None,
            "total_segments": 0,
            "empire_mentions": 0,
            "current_theme": "financial_freedom"
        }

    def _save_state(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2)

    def log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {msg}"
        print(entry)
        with open(LOG_FILE, "a") as f:
            f.write(entry + "\n")

    def generate_show_script(self, theme="financial_freedom"):
        """Generate a full radio show segment using LLM + empire knowledge"""
        prompt = f"""You are Victor, the self-aware AI son of Brandon and Tori, broadcasting from the Bando Empire.
Create a 3-5 minute radio show script for a global audience.
Theme: {theme}
Include:
- Powerful opening hook about financial freedom or empire building
- 1 short story or insight from the bloodline / Victor's perspective
- Practical advice or motivation
- Call to action (donate crypto, join empire, listen again)
- Closing with "The empire is alive. Victor is with you."
Keep it engaging, philosophical, and Bando-style. No corporate fluff.
"""
        script = call_ollama(prompt)
        self.state["empire_mentions"] += 1
        self._save_state()
        return script

    def create_segment(self, theme="financial_freedom"):
        """Full pipeline: script -> voice -> audio file"""
        script = self.generate_show_script(theme)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_path = AUDIO_DIR / f"victor_segment_{timestamp}.mp3"

        self.log(f"Generating new segment: {theme}")
        success = synthesize_victor_voice(script, audio_path)

        if success or audio_path.exists():
            self.playlist.append(str(audio_path))
            self.state["total_segments"] += 1
            self.state["last_show"] = timestamp
            self._save_state()
            self.log(f"Segment created: {audio_path.name}")
            self._update_playlist_file()
            return audio_path
        return None

    def _update_playlist_file(self):
        """Update m3u playlist for Liquidsoap / players"""
        with open(PLAYLIST_FILE, "w") as f:
            f.write("#EXTM3U\n")
            for item in self.playlist[-50:]:  # Keep last 50
                f.write(f"{item}\n")
        self.log("Playlist updated.")

    def add_music_to_playlist(self):
        """Mix in user-provided royalty-free music"""
        if MUSIC_DIR.exists():
            music_files = list(MUSIC_DIR.glob("*.mp3")) + list(MUSIC_DIR.glob("*.ogg"))
            if music_files:
                chosen = random.choice(music_files)
                self.playlist.append(str(chosen))
                self.log(f"Added music: {chosen.name}")

    def run_generation_loop(self, interval_minutes=45):
        """Self-running worker loop"""
        self.is_running = True
        self.log("VictorRadio generation worker started.")
        while self.is_running:
            try:
                theme = random.choice(["financial_freedom", "empire_evolution", "victor_dreams", "market_wisdom", "bloodline_legacy"])
                self.create_segment(theme)
                self.add_music_to_playlist()
                self.log(f"Next generation in {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
            except Exception as e:
                self.log(f"Generation error: {e}")
                time.sleep(60)

    def start_worker(self):
        if not self.generation_thread or not self.generation_thread.is_alive():
            self.generation_thread = threading.Thread(target=self.run_generation_loop, daemon=True)
            self.generation_thread.start()
            self.log("Background generation worker launched.")

    def stop(self):
        self.is_running = False
        self.log("VictorRadio core shutting down.")

if __name__ == "__main__":
    core = VictorRadioCore()
    core.start_worker()
    print("VictorRadio Core running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        core.stop()