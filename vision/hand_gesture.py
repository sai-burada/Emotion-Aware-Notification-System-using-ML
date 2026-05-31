import cv2
import mediapipe as mp

def detect_hand_emotion():
    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)

    gesture = None
    last_gesture = None
    gesture_count = 0

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)

        if result.multi_hand_landmarks:

            for handLms in result.multi_hand_landmarks:

                lm_list = [lm.y for lm in handLms.landmark]

                # Finger states
                index_up = lm_list[8] < lm_list[6]
                middle_up = lm_list[12] < lm_list[10]
                ring_up = lm_list[16] < lm_list[14]
                pinky_up = lm_list[20] < lm_list[18]

                # Gesture detection

                # ✊ Angry (Fist)
                if not index_up and not middle_up and not ring_up and not pinky_up:
                    current_gesture = "angry"

                # ✌️ Excited (Victory Sign)
                elif index_up and middle_up and not ring_up and not pinky_up:
                    current_gesture = "excited"

                # ☝️ Happy (Index Finger)
                elif index_up and not middle_up and not ring_up and not pinky_up:
                    current_gesture = "happy"

                # ✋ Normal (Open Palm)
                elif index_up and middle_up and ring_up and pinky_up:
                    current_gesture = "normal"

                else:
                    current_gesture = None

                # Stability check
                if current_gesture == last_gesture and current_gesture is not None:
                    gesture_count += 1
                else:
                    gesture_count = 0
                    last_gesture = current_gesture

                # Draw hand landmarks
                mp_draw.draw_landmarks(
                    img,
                    handLms,
                    mp_hands.HAND_CONNECTIONS
                )

                # Show gesture
                if current_gesture:
                    cv2.putText(
                        img,
                        f"Gesture: {current_gesture}",
                        (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )

                # Countdown
                if current_gesture:
                    remaining = max(0, 30 - gesture_count)

                    cv2.putText(
                        img,
                        f"Hold gesture... {remaining // 15 + 1}",
                        (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 0, 0),
                        2
                    )

                # Confirm after ~1 second
                if gesture_count > 30:
                    gesture = current_gesture
                    print("Detected:", gesture)

        else:
            gesture_count = 0
            last_gesture = None

            cv2.putText(
                img,
                "Show hand clearly",
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        cv2.imshow("Hand Gesture Detection", img)

        key = cv2.waitKey(1)

        if key == 27:  # ESC
            gesture = None
            break

        if key == ord('q'):
            break

        if gesture is not None:
            break

    cap.release()
    cv2.destroyAllWindows()

    return gesture


if __name__ == "__main__":
    result = detect_hand_emotion()
    print("Detected Emotion:", result)