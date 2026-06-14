from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
from scipy.signal import resample

# 1. Configuration
DEVICE_ID = 4
NATIVE_FS = 48000  # The rate your hardware actually likes
TARGET_FS = 16000  # The rate Whisper needs
DURATION = 5

print("Loading model...")
model = WhisperModel("base", device="cpu", compute_type="int8")

# 2. Record at the NATIVE rate
print(f"Listening at {NATIVE_FS}Hz...")
raw_recording = sd.rec(
    int(DURATION * NATIVE_FS), 
    samplerate=NATIVE_FS, 
    channels=1, 
    device=DEVICE_ID, 
    dtype='float32'
)
sd.wait()

# 3. Resample to 16kHz
num_samples = int(len(raw_recording) * TARGET_FS / NATIVE_FS)
audio_data = resample(raw_recording.flatten(), num_samples)

print("Transcribing...")
segments, _ = model.transcribe(audio_data, beam_size=5)

results = list(segments)
if not results:
    print("No speech detected.")
else:
    for segment in results:
        print(f"Result: {segment.text}")