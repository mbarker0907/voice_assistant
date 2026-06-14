import sounddevice as sd
import numpy as np
from scipy.signal import resample
import queue

MIC_DEVICE_ID = 4
audio_queue = queue.Queue()

# Ask the hardware for its native rate
device_info = sd.query_devices(MIC_DEVICE_ID, 'input')
HW_SAMPLE_RATE = int(device_info['default_samplerate'])

def callback(indata, frames, time, status):
    audio_queue.put(indata[:, 0].copy())

print("--- Push-to-Talk (Instant Start) ---")
print("Recording started! Speak now...")
print("Press ENTER to STOP recording...")

# Start recording
with sd.InputStream(samplerate=HW_SAMPLE_RATE, channels=1, dtype='float32', device=MIC_DEVICE_ID, callback=callback):
    input() 

print("Saving audio for Engine...")

audio_data = []
while not audio_queue.empty():
    audio_data.append(audio_queue.get())

if audio_data:
    recording = np.concatenate(audio_data, axis=0).flatten()
    num_samples = int(len(recording) * 16000 / HW_SAMPLE_RATE)
    recording = resample(recording, num_samples)
    
    try:
        np.save("/tmp/transcribe_data.npy", recording)
        print("Sent to Engine!")
    except Exception as e:
        print(f"Error saving file: {e}")
else:
    print("Error: No audio data captured.")