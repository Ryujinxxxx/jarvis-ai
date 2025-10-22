# ==============================================
# JARVIS SERVER - Windows Compatible with LocalTunnel
# ==============================================

from flask import Flask, request, jsonify
import subprocess
import threading
import os
import sys
import time
import requests

# ==============================================
# CONFIGURATION
# ==============================================
AI_NAME = "Jarvis"
OLLAMA_URL = "http://127.0.0.1:11434/v1/completions"
OLLAMA_MODEL = "llama3.2"

# ==============================================
# FLASK APP
# ==============================================
app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"response": "No prompt provided"})
    # Call your AI logic
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=20
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["text"]
        return jsonify({"response": text.strip() if text else "No answer from AI"})
    except Exception as e:
        return jsonify({"response": f"AI Error: {e}"})

# ==============================================
# LOCALTUNNEL SETUP (Windows)
# ==============================================
def run_localtunnel(port=5000, subdomain="jarvisai"):
    # REPLACE this path with your actual npm global lt.cmd path
    lt_cmd_path = r"C:\Users\mfahm\AppData\Roaming\npm\lt.cmd"

    if not os.path.isfile(lt_cmd_path):
        print("❌ LocalTunnel (lt.cmd) not found. Make sure you installed it with 'npm install -g localtunnel'")
        sys.exit(1)

    try:
        process = subprocess.Popen(
            [lt_cmd_path, "--port", str(port), "--subdomain", subdomain],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True  # needed for .cmd
        )

        print("🌐 Waiting for LocalTunnel to provide public URL...")
        public_url = None

        while True:
            line = process.stdout.readline()
            if not line:
                break
            line = line.strip()
            # Detect public URL line
            if "your url is:" in line.lower():
                public_url = line.split("your url is:")[-1].strip()
                print(f"✅ Jarvis is now accessible at: {public_url}")
                break
        if not public_url:
            print("❌ Could not get public URL from LocalTunnel output.")
        return process

    except Exception as e:
        print(f"❌ Failed to start LocalTunnel: {e}")
        sys.exit(1)

# ==============================================
# RUN SERVER
# ==============================================
if __name__ == "__main__":
    # Start LocalTunnel in a separate thread
    lt_thread = threading.Thread(target=run_localtunnel, args=(5000, "jarvisai"), daemon=True)
    lt_thread.start()

    # Start Flask
    print("🚀 Starting Jarvis server...")
    app.run(host="0.0.0.0", port=5000)
