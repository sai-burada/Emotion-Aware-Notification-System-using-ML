def decide_notification(emotion):
    if emotion == "angry":
        return "BLOCK ❌"
    elif emotion == "sad":
        return "LIMIT 💙"
    elif emotion == "happy":
        return "NORMAL 😊"
    else:
        return "SHOW ALL 🔥"