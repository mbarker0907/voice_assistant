import sounddevice as sd
import numpy as np

device_id = 4
# Query the device's default settings
device_info = sd.query_devices(device_id, 'input')
fs = int(device_info['default_samplerate'])

print(f"Recording for 5 seconds using device ID {device_id} at {fs}Hz...")

recording = sd.rec(int(5 * fs), samplerate=fs, channels=1, device=device_id, dtype='float32')
sd.wait()
print("Recording finished successfully!")