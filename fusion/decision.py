def final_emotion(face, hand):

    if face == "angry" or hand == "angry":
        return "angry"

    elif face == "happy" or hand == "happy":
        return "happy"

    elif face == "excited" or hand == "excited":
        return "excited"

    elif face == "sad" or hand == "sad":
        return "sad"

    else:
        return "normal"