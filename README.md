Voice Scribe
A fast, private, and local voice-to-text tool for Linux, powered by Whisper and refined by Google Gemini.

Voice Scribe lets you speak your thoughts and instantly have them converted into polished text on your clipboard, ready to paste anywhere.

Why it’s different:
No more "stop-listening" lag: You control exactly when to start and stop recording.

100% Private: Your voice is processed locally on your machine.

AI Polished: Your raw dictation is automatically cleaned up by Gemini for perfect grammar and flow before it hits your clipboard.

Instant Productivity: One keyboard shortcut to record, one hit of the Enter key to transcribe.

How it works:
Trigger: Start the script via terminal.

Record: Speak your thoughts.

Polish: The script transcribes your audio locally, then sends it to Gemini to fix punctuation and flow.

Clipboard: Your finalized, professional text is instantly copied to your clipboard.

Setup & Configuration
1. Requirements
Ensure you have Python installed and the following libraries:

Bash
pip install sounddevice numpy faster-whisper pyperclip google-genai
2. Configure your Microphone
Since audio device IDs vary by system, you must configure the script to use your specific microphone:

Open your terminal and run:

Bash
python3 -m sounddevice
Identify your input device from the list (look for a device with in channels). Note the index number (e.g., 4).

Open transcribe.py and update the MIC_DEVICE_ID variable:

Python
MIC_DEVICE_ID = 4  # Change this to your ID
3. API Key Setup
This script uses the Gemini API to polish your transcripts.

Get an API key from Google AI Studio.

In transcribe.py, paste your key into the GEMINI_API_KEY variable:

Python
GEMINI_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
Usage
Simply run the script:

Bash
python transcribe.py
Press ENTER to start, speak, and press ENTER again to stop. Your polished text will be ready to paste!