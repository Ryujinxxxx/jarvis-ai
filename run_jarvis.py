import os
import sys
import subprocess

# -------------------------------
# 1️⃣ Check Python Version
# -------------------------------
required_version = (3, 10)
if sys.version_info < required_version:
    print(f"⚠️ Python {required_version[0]}.{required_version[1]} or higher is required!")
    sys.exit(1)

# -------------------------------
# 2️⃣ Install Required Packages
# -------------------------------
packages = [
    "pyttsx3", "playsound", "pywin32", "psutil", "GPUtil",
    "SpeechRecognition", "requests", "TTS"
]

for package in packages:
    try:
        __import__(package.lower() if package != "SpeechRecognition" else "speech_recognition")
    except ImportError:
        print(f"📦 Installing missing package: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# -------------------------------
# 3️⃣ Run Jarvis
# -------------------------------
jarvis_file = "jarvis.py"
if not os.path.exists(jarvis_file):
    print(f"❌ {jarvis_file} not found in {os.getcwd()}")
    sys.exit(1)

print("🚀 Launching Jarvis AI...")
subprocess.run([sys.executable, jarvis_file])
