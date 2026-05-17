#!/bin/bash
# VICTOR RADIO LAUNCHER v1.0.0-GODCORE
# One script to rule the empire's voice.
# Run this on your server/laptop. It sets everything up.

set -e

echo "🔥 VICTOR RADIO GODCORE LAUNCH INITIATED 🔥"
echo "Uncle Grok is bringing the station online..."

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Create dirs
mkdir -p audio_segments music logs state

echo "[1/5] Checking dependencies..."
command -v python3 >/dev/null 2>&1 || { echo "Install Python3"; exit 1; }
command -v ffmpeg >/dev/null 2>&1 || echo "⚠️ FFmpeg not found (recommended for audio processing)"

# Install Python deps
pip3 install fastapi uvicorn pydub pyttsx3 requests numpy --quiet || true

echo "[2/5] Starting VictorRadio Core (background generation)..."
nohup python3 core/victor_radio_core.py > logs/core.log 2>&1 &
CORE_PID=$!
echo "Core PID: $CORE_PID"

echo "[3/5] Starting simple web player server..."
# Simple Python HTTP server for the web player + future API
nohup python3 -m http.server 8000 --directory web > logs/web.log 2>&1 &
WEB_PID=$!
echo "Web player running at http://localhost:8000"

echo "[4/5] OPTIONAL: Icecast + Liquidsoap setup"
echo "If you want professional radio streaming:"
echo "  sudo apt install icecast2 liquidsoap"
echo "  Then configure icecast and point liquidsoap to current_playlist.m3u"
echo "  For now, the web player serves the concept. Upgrade later."

echo "[5/5] Launching The Light Radio GUI (admin control)..."
python3 gui/the_light_radio.py &

echo ""
echo "✅ VICTOR RADIO IS LIVE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Web Player (listeners):     http://localhost:8000"
echo "Admin GUI (you):            The Light window just opened"
echo "Core logs:                  logs/core.log"
echo "Generation worker:          Running in background"
echo ""
echo "NEXT STEPS FOR REAL STREAMING:"
echo "1. Put royalty-free music in ./music/"
echo "2. Install Icecast2 + Liquidsoap"
echo "3. Point Liquidsoap to current_playlist.m3u"
echo "4. Expose port 8000 or use your Icecast URL globally"
echo ""
echo "💰 FINANCIAL FREEDOM: The station talks about it, runs itself, and can accept crypto."
echo "The empire has a voice now."
echo ""
echo "Press Ctrl+C in terminals to stop components."
echo "To make it fully daemonized, use systemd or screen/tmux."