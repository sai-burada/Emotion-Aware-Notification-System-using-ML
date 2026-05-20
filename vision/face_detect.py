import cv2

def capture_face():
    cam = cv2.VideoCapture(0)

    print("Press 'q' to capture image...")

    while True:
        ret, frame = cam.read()
        cv2.imshow("Camera - Press Q to Capture", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("face.jpg", frame)
            print("Image Captured ✅")
            break

    cam.release()
    cv2.destroyAllWindows()