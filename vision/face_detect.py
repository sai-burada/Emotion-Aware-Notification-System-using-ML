import cv2

def capture_face():
    cam = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    print("Face Detection Started")
    print("Press Q only when your face is detected")

    while True:
        ret, frame = cam.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100)
        )

        face_found = False

        for (x, y, w, h) in faces:
            face_found = True

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Face Detected",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        if not face_found:
            cv2.putText(
                frame,
                "No Face Detected",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):

            if face_found:
                cv2.imwrite("face.jpg", frame)
                print("Face Captured Successfully")
                break
            else:
                print("No face detected. Move closer to camera.")

        if key == 27:  # ESC
            break

    cam.release()
    cv2.destroyAllWindows()