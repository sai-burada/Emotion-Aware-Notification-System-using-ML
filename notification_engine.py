def decide_notification(emotion):

    if emotion == "angry":
        return "BLOCK Social Media Notifications"

    elif emotion == "sad":
        return "Show Important Notifications Only"

    elif emotion == "normal":
        return "Show All Notifications"

    elif emotion == "happy":
        return "Show All Notifications"

    elif emotion == "excited":
        return "Show Priority Notifications Only"

    else:
        return "No Action"