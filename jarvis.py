# ==============================================
# JARVIS AI - Full Version
# ==============================================

import os
import threading
import pyttsx3
import speech_recognition as sr
import platform
import psutil
import GPUtil
import datetime
import requests
import json
import tkinter as tk
from tkinter import scrolledtext

# ==============================================
# CONFIGURATION
# ==============================================
AI_NAME = "Jarvis"
OLLAMA_URL = "http://127.0.0.1:11434/v1/completions"
OLLAMA_MODEL = "llama3.2"

# ==============================================
# INITIALIZE TTS
# ==============================================
engine = pyttsx3.init()
engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
for voice in voices:
    if "english" in voice.name.lower() and ("male" in voice.name.lower() or "david" in voice.name.lower()):
        engine.setProperty("voice", voice.id)
        break

def speak(text):
    """Threaded TTS to speak without blocking GUI"""
    def run():
        engine.say(text)
        engine.runAndWait()
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()

# ==============================================
# MICROPHONE CHECK
# ==============================================
try:
    sr.Microphone()
    MIC_AVAILABLE = True
except OSError:
    MIC_AVAILABLE = False

recognizer = sr.Recognizer()

def listen_command():
    if not MIC_AVAILABLE:
        chat_box_insert("⚠️ Microphone not available.")
        return ""
    with sr.Microphone() as source:
        chat_box_insert("🎧 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        command = recognizer.recognize_google(audio)
        chat_box_insert(f"🗣️ You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        chat_box_insert("⚠️ Could not understand audio.")
        return ""
    except sr.RequestError:
        chat_box_insert("⚠️ Speech recognition unavailable.")
        return ""

# ==============================================
# AI QUERY
# ==============================================
def ask_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=20
        )
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["text"]
        return text.strip() if text else "I'm unable to answer right now, Sir."
    except Exception as e:
        return f"AI Error: {e}"

# ==============================================
# SYSTEM INFO
# ==============================================
def system_info():
    battery = psutil.sensors_battery()
    gpus = GPUtil.getGPUs()
    info = {
        "OS": f"{platform.system()} {platform.release()}",
        "CPU": platform.processor(),
        "Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "RAM (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "GPU": gpus[0].name if gpus else "No GPU detected",
        "Battery": f"{battery.percent}% {'Charging' if battery.power_plugged else 'Not Charging'}" if battery else "No battery info",
        "Time": datetime.datetime.now().strftime("%I:%M %p"),
        "Date": datetime.datetime.now().strftime("%A, %B %d, %Y")
    }
    return info

# ==============================================
# GUI HELPER
# ==============================================
def chat_box_insert(message):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"{message}\n")
    chat_box.see(tk.END)
    chat_box.config(state=tk.DISABLED)

# ==============================================
# PROCESS COMMAND
# ==============================================
def process_command(command):
    command = command.lower()
    if any(k in command for k in ["exit", "quit", "shutdown", "stop"]):
        speak("Shutting down systems. Goodbye, Sir.")
        root.quit()
        return "EXIT"
    if "time" in command:
        reply = f"The time is {datetime.datetime.now().strftime('%I:%M %p')}, Sir."
        speak(reply)
        return reply
    if "date" in command:
        reply = f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}, Sir."
        speak(reply)
        return reply
    if "system" in command or "info" in command:
        info = system_info()
        reply = "\n".join(f"{k}: {v}" for k, v in info.items())
        speak("Displaying system information, Sir.")
        return reply

    # fallback to AI
    speak("Processing your request, Sir.")
    reply = ask_ollama(command)
    speak(reply)
    return reply

# ==============================================
# GUI CALLBACKS
# ==============================================
def on_send():
    command = input_box.get().strip()
    if not command:
        return
    input_box.delete(0, tk.END)
    chat_box_insert(f">>> {command}")
    reply = process_command(command)
    chat_box_insert(f"🤖 {AI_NAME}: {reply}")

def on_voice():
    command = listen_command()
    if not command:
        return
    reply = process_command(command)
    chat_box_insert(f"🤖 {AI_NAME}: {reply}")

# ==============================================
# GUI SETUP
# ==============================================
root = tk.Tk()
root.title(f"{AI_NAME} AI Assistant")
root.geometry("700x500")
root.resizable(False, False)

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=85, height=25, font=("Consolas", 11))
chat_box.pack(padx=10, pady=10)
chat_box.config(state=tk.DISABLED)
chat_box_insert(f"==================================================")
chat_box_insert(f"       {AI_NAME.upper()} AI SYSTEM - ONLINE")
chat_box_insert(f"==================================================\n")
greeting = f"Hello Sir, {AI_NAME} is online and ready to operate."
chat_box_insert(f"🤖 {AI_NAME}: {greeting}")
speak(greeting)

# Input frame
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=5)

input_box = tk.Entry(input_frame, width=60, font=("Consolas", 11))
input_box.pack(side=tk.LEFT, padx=5)
input_box.focus()

send_button = tk.Button(input_frame, text="Send", command=on_send)
send_button.pack(side=tk.LEFT, padx=5)

voice_button = tk.Button(input_frame, text="Voice Command", command=on_voice)
voice_button.pack(side=tk.LEFT, padx=5)

exit_button = tk.Button(input_frame, text="Exit", command=root.quit)
exit_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
