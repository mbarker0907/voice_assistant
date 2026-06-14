import time
import os
import numpy as np
from faster_whisper import WhisperModel
import pyperclip

print("Loading Whisper model into memory... please wait.")
model = WhisperModel("base", device="cpu", compute_type="int8")
print("Engine is ready and waiting for audio data...")

AUDIO_FILE = "/tmp/transcribe_data.npy"

while True:
    if os.path.exists(AUDIO_FILE):
        print("\n[Engine] Transcribing...")
        time.sleep(0.15) 
        
        try:
            recording = np.load(AUDIO_FILE)
            os.remove(AUDIO_FILE)
            
            segments, _ = model.transcribe(recording, beam_size=5)
            full_text = " ".join([s.text for s in segments]).strip()
            
            if full_text:
                pyperclip.copy(full_text)
                print(f"Transcription: {full_text}")
                print("[✓] Copied to clipboard!")
            else:
                print("(No speech detected)")
                
        except Exception as e:
            print(f"\n[ERROR] Engine error: {e}")
            if os.path.exists(AUDIO_FILE):
                os.remove(AUDIO_FILE)
                
    time.sleep(0.5)