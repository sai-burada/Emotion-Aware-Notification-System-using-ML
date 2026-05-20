import cv2
import mediapipe as mp

def detect_hand_emotion():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    gesture = None

    while True:
        success, img = cap.read()
        if not success:
            break

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                lm_list = [lm.y for lm in handLms.landmark]

                # 👉 Finger conditions
                index_up = lm_list[8] < lm_list[6]
                middle_up = lm_list[12] < lm_list[10]
                ring_up = lm_list[16] < lm_list[14]
                pinky_up = lm_list[20] < lm_list[18]
                thumb_up = lm_list[4] < lm_list[3]

                # ✊ PUNCH (FIST) = ANGRY
                if (not index_up and not middle_up and not ring_up and not pinky_up):
                    gesture = "angry (punch)"

                # 😊 HAPPY → Index finger up
                elif index_up and not middle_up:
                    gesture = "happy"

                # 🤩 EXCITED → Thumb up
                elif thumb_up:
                    gesture = "excited"

                # 😐 NORMAL
                else:
                    gesture = "normal"

                mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

        # Show text on screen
        if gesture:
            cv2.putText(img, f'Gesture: {gesture}', (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Hand Gesture", img)

        key = cv2.waitKey(1)

        # ESC key
        if key == 27:
            print("Stopped by user")
            gesture = None
            break

        # 'q' key
        if key == ord('q'):
            print("Quit pressed")
            break

        if gesture is not None:
            break

    cap.release()
    cv2.destroyAllWindows()

    return gesture


# Run function
if __name__ == "__main__":
    result = detect_hand_emotion()
    print("Detected Emotion:", result)