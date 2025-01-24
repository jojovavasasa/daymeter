@echo off
start /wait powershell -Command "ollama pull llama2:7b"
python -m pip install SpeechRecognition pyaudio
