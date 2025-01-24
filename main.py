MODEL_NAME = "llama2:7b"
PROMPT = "Rate from 1 to 10 how good my day was based on the following information:"

import tkinter as tk
from tkinter import messagebox
import subprocess
import speech_recognition as sr

def analyze_day(input_text):
    try:
        # Add the prompt to the user's input
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME],
            input=f"{PROMPT} {input_text}",
            text=True,
            capture_output=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def submit_text():
    user_input = text_input.get("1.0", "end-1c")
    if not user_input.strip():
        messagebox.showerror("Error", "Please enter something about your day!")
        return
    output = analyze_day(user_input)
    result_label.config(text=f"Score: {output}")

def use_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Listening...", "Tell me about your day.")
        try:
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio)
            output = analyze_day(user_input)
            result_label.config(text=f"Score: {output}")
        except sr.UnknownValueError:
            messagebox.showerror("Error", "I couldn't understand you.")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Speech recognition isn't working: {e}")

def quit_app():
    root.quit()

root = tk.Tk()
root.title("DayMeter")

# Set window to fullscreen
root.attributes("-fullscreen", True)

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

instructions = tk.Label(root, text="Type or tell me how your day was:")
canvas.create_window(200, 20, window=instructions)

text_input = tk.Text(root, height=5, width=40)
canvas.create_window(200, 80, window=text_input)

button_frame = tk.Frame(root)
canvas.create_window(200, 160, window=button_frame)

submit_button = tk.Button(button_frame, text="Submit", command=submit_text)
submit_button.grid(row=0, column=0, padx=5)

mic_button = tk.Button(button_frame, text="🎤 Use Microphone", command=use_microphone)
mic_button.grid(row=0, column=1, padx=5)

quit_button = tk.Button(button_frame, text="Quit", command=quit_app)
quit_button.grid(row=1, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="Score will appear here.")
canvas.create_window(200, 250, window=result_label)

root.mainloop()
