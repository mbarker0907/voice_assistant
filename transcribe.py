import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import queue
import pyperclip
import os
from google import genai

# --- CONFIGURATION ---
# Ensure your API key is set in your terminal: 
# export GEMINI_API_KEY="Enter Your Google API KEY Here Without Quotes"
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Use "large-v3" for high accuracy
model = WhisperModel("large-v3", device="cpu", compute_type="int8")

MIC_DEVICE_ID = 4
TARGET_SAMPLE_RATE = 16000 
audio_queue = queue.Queue()

def callback(indata, frames, time, status):
    audio_queue.put(indata.copy())

def fix_grammar(text):
    """Sends raw transcript to Gemini for a quick polish."""
    prompt = (f"Fix the grammar, punctuation, and flow of the following transcription. "
              f"Return ONLY the corrected text. Do not add conversational filler:\n\n{text}")
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=prompt
    )
    return response.text

# --- MAIN EXECUTION ---
print("--- Voice Scribe (High Accuracy + AI Polish) ---")
print("Press ENTER to START recording...")
input()
print("Recording... (Press ENTER again to STOP)")

with sd.InputStream(samplerate=TARGET_SAMPLE_RATE, channels=1, dtype='float32', device=MIC_DEVICE_ID, callback=callback):
    input()

print("Processing with Whisper...")
audio_data = []
while not audio_queue.empty():
    audio_data.append(audio_queue.get())

if audio_data:
    recording = np.concatenate(audio_data, axis=0).flatten()
    
    # Transcribe
    segments, info = model.transcribe(recording, beam_size=5, language="en")
    raw_text = "".join([segment.text for segment in segments]).strip()
    
    print("\n[Raw Transcription]:")
    print(raw_text)

    # Polish with Gemini
    print("\nPolishing with Gemini...")
    polished_text = fix_grammar(raw_text)
    
    print("\n--- Final Polished Text ---")
    print(polished_text)
    
    pyperclip.copy(polished_text)
    print("\n[✓] Polished text copied to clipboard!")
else:
    print("No audio recorded.")