import sys
import os
import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3   # 🔊 voice assistant

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports
from vision.hand_gesture import detect_hand_emotion
from speech.audio_input import record_audio
from speech.speech_features import extract_features
from speech.speech_predict import predict_speech

from vision.face_detect import capture_face
from vision.face_predict import predict_face

# ❌ removed unused final_emotion import
from notification_generator import get_notification
from notification_engine import decide_notification


# 🔊 Voice Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)


def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Speech error:", e)


# 🤖 AI Suggestion
def suggest_action(emotion):
    actions = {
        "angry": "You seem angry. Please take deep breaths and relax.",
        "sad": "You seem sad. Try listening to music or talking to a friend.",
        "happy": "You are happy. Keep smiling and enjoy your moment.",
        "normal": "You are in a normal mood. Stay focused and continue your work.",
        "excited": "You are excited. Use this energy in something productive."
    }
    return actions.get(emotion, "Stay calm and balanced.")


def run_system():
    status.set("Opening Camera... 📸")
    root.update_idletasks()

    capture_face()

    # ✅ Camera check
    if not os.path.exists("face.jpg") or os.path.getsize("face.jpg") == 0:
        msg = "Camera not working. Please check your webcam."
        result.set(msg)
        speak(msg)
        status.set("Camera Error ❌")
        return

    # ✅ Load image safely
    try:
        img = Image.open("face.jpg")
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)

        image_label.config(image=img_tk)
        image_label.image = img_tk
    except Exception as e:
        print("Image error:", e)
        msg = "Image not clear. Adjust lighting and face the camera."
        result.set(msg)
        speak(msg)
        status.set("Image Error ❌")
        return

    # ✋ Hand Gesture
    status.set("Detecting Hand Gesture... ✋")
    root.update_idletasks()

    try:
        hand_emotion = detect_hand_emotion()
    except Exception as e:
        print("Hand gesture error:", e)
        hand_emotion = None

    if hand_emotion is None:
        msg = "Hand gesture not detected. Show your hand clearly."
        result.set(msg)
        speak(msg)
        status.set("Gesture Error ❌")
        return

    # 🎤 Audio
    status.set("Recording Audio... 🎤")
    root.update_idletasks()

    try:
        record_audio("voice.wav")
    except Exception as e:
        print("Audio error:", e)
        msg = "Microphone error. Please check your mic."
        result.set(msg)
        speak(msg)
        status.set("Audio Error ❌")
        return

    status.set("Voice Recorded ✅")
    root.update_idletasks()

    # 🎤 Speech Emotion
    try:
        features = extract_features("voice.wav")
        speech_emotion = predict_speech(features)
    except Exception as e:
        print("Speech model error:", e)
        speech_emotion = "normal"

    # 👤 Face Emotion
    try:
        face_emotion = predict_face()
    except Exception as e:
        print("Face model error:", e)
        face_emotion = None

    if face_emotion is None or face_emotion == "no_face":
        msg = "Face not detected clearly. Sit in good lighting and face the camera."
        result.set(msg)
        speak(msg)
        status.set("Face Error ❌")
        return

    # 🧠 FINAL DECISION (Fusion)
    emotions = [face_emotion, speech_emotion, hand_emotion]
    final = max(set(emotions), key=emotions.count)

    # 🔔 Notification
    try:
        notif = get_notification()
        decision = decide_notification(final)
    except Exception as e:
        print("Notification error:", e)
        notif = {"app": "N/A", "msg": "No message"}
        decision = "No action"

    # 🤖 Suggestion
    action = suggest_action(final)

    # 🖥️ Display
    result.set(f"""
Face: {face_emotion}
Voice: {speech_emotion}
Hand: {hand_emotion}

Final Emotion: {final}

Suggestion:
{action}

App: {notif['app']}
Message: {notif['msg']}

Decision: {decision}
""")

    # 🔊 Speak
    speak(f"Your emotion is {final}. {action}")

    status.set("Done ✅")


# 🎨 GUI
root = tk.Tk()
root.title("Emotion AI Notification System")
root.geometry("550x600")
root.configure(bg="#1e1e2f")

title = tk.Label(root,
                 text="Emotion AI Notification System",
                 font=("Arial", 18, "bold"),
                 bg="#1e1e2f", fg="white")
title.pack(pady=15)

status = tk.StringVar()
status.set("Click Start")

status_label = tk.Label(root,
                        textvariable=status,
                        font=("Arial", 12),
                        bg="#1e1e2f", fg="lightblue")
status_label.pack(pady=5)

# 📸 Image
image_label = tk.Label(root, bg="#1e1e2f")
image_label.pack(pady=10)

result = tk.StringVar()

result_label = tk.Label(root,
                        textvariable=result,
                        font=("Arial", 11),
                        bg="#1e1e2f",
                        fg="white",
                        justify="left",
                        wraplength=500)
result_label.pack(pady=20)

start_btn = tk.Button(root,
                      text="Start Detection",
                      command=run_system,
                      font=("Arial", 12, "bold"),
                      bg="#4CAF50",
                      fg="white",
                      padx=10,
                      pady=5)

start_btn.pack(pady=20)

root.mainloop()