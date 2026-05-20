import random

emotions = ["angry", "sad", "normal", "happy", "excited"]

def predict_speech(features):
    return random.choice(emotions)