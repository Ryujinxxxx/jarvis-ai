@echo off
:: Activate Python 3.10 (adjust path if needed)
SET PYTHON=C:\Users\mfahm\AppData\Local\Programs\Python\Python310\python.exe

:: Install missing packages automatically
%PYTHON% -m pip install --upgrade pyttsx3 playsound pywin32 psutil GPUtil SpeechRecognition requests simpleaudio

:: Run Jarvis
%PYTHON% jarvis.py

pause
