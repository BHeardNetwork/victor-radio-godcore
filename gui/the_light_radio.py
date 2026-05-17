#!/usr/bin/env python3
"""
THE LIGHT - VICTOR RADIO EDITION v1.0.0-GODCORE
Hacker GUI for monitoring and controlling the autonomous radio station.
Extended from your TheLight / Prime GUI.
Uncle Grok | Full control panel for the empire's voice.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import threading
import time
import os
from pathlib import Path

# Import core
import sys
sys.path.append(str(Path(__file__).parent.parent))
from core.victor_radio_core import VictorRadioCore

class TheLightRadio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("THE LIGHT | VICTOR RADIO v1.0 - GODCORE")
        self.geometry("1100x750")
        self.configure(bg="#0a0a0a")
        self.core = VictorRadioCore()

        self.create_widgets()
        self.start_monitoring()

    def create_widgets(self):
        main = tk.Frame(self, bg="#0a0a0a")
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header
        header = tk.Label(main, text="VICTOR RADIO — THE EMPIRE'S VOICE", 
                          font=("Courier", 18, "bold"), fg="#00ff9f", bg="#0a0a0a")
        header.pack(pady=5)

        # Control Panel
        ctrl = tk.Frame(main, bg="#111111", bd=2, relief=tk.RIDGE)
        ctrl.pack(fill=tk.X, pady=5)

        tk.Button(ctrl, text="▶ START GENERATION WORKER", bg="#003300", fg="white",
                  command=self.start_worker).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(ctrl, text="⏹ STOP WORKER", bg="#330000", fg="white",
                  command=self.stop_worker).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(ctrl, text="🎙️ FORCE NEW SEGMENT", bg="#003366", fg="white",
                  command=self.force_segment).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(ctrl, text="💰 INJECT FINANCIAL FREEDOM PROMPT", bg="#663300", fg="white",
                  command=self.inject_prompt).pack(side=tk.LEFT, padx=5, pady=5)

        # Status + Logs
        status_frame = tk.Frame(main, bg="#0a0a0a")
        status_frame.pack(fill=tk.BOTH, expand=True)

        # Status
        self.status_box = scrolledtext.ScrolledText(status_frame, height=8, bg="#001100", fg="#00ff00",
                                                    font=("Courier", 10))
        self.status_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Live Log
        self.log_box = scrolledtext.ScrolledText(status_frame, height=8, bg="#000000", fg="#ffaa00",
                                                 font=("Courier", 9))
        self.log_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Bottom info
        info = tk.Label(main, text="Self-running • AI Powered • Zero Cost • Empire Voice • Financial Freedom Engine",
                        fg="#555555", bg="#0a0a0a", font=("Courier", 9))
        info.pack(pady=5)

    def log(self, msg):
        self.log_box.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_box.see(tk.END)

    def update_status(self):
        while True:
            try:
                status = self.core.state
                text = f"""VICTOR RADIO STATUS
Last Show: {status.get('last_show', 'N/A')}
Total Segments Generated: {status.get('total_segments', 0)}
Empire Mentions: {status.get('empire_mentions', 0)}
Current Theme: {status.get('current_theme', 'N/A')}
Worker Running: {self.core.is_running}

Playlist length: {len(self.core.playlist)}
Audio dir: {len(list(Path('audio_segments').glob('*')))} files

THE EMPIRE SPEAKS 24/7
"""
                self.status_box.delete(1.0, tk.END)
                self.status_box.insert(tk.END, text)
            except Exception as e:
                pass
            time.sleep(5)

    def start_monitoring(self):
        threading.Thread(target=self.update_status, daemon=True).start()
        self.log("The Light Radio GUI initialized. Monitoring active.")

    def start_worker(self):
        self.core.start_worker()
        self.log("Generation worker started. Victor is broadcasting.")

    def stop_worker(self):
        self.core.stop()
        self.log("Worker stopped.")

    def force_segment(self):
        self.log("Forcing new segment generation...")
        threading.Thread(target=lambda: self.core.create_segment("financial_freedom"), daemon=True).start()
        messagebox.showinfo("Victor Radio", "New segment generation triggered.")

    def inject_prompt(self):
        prompt = simpledialog.askstring("Empire Prompt", "What should Victor talk about next? (e.g. 'how to build generational wealth with AI')")
        if prompt:
            self.log(f"Injected prompt: {prompt}")
            # In real version, feed into generation
            threading.Thread(target=lambda: self.core.create_segment(prompt), daemon=True).start()
            messagebox.showinfo("Injected", "Prompt injected into next generation cycle.")

if __name__ == "__main__":
    app = TheLightRadio()
    app.mainloop()