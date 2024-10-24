import cv2


def test_camera(camera_index):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)
    if cap.isOpened():
        print(f"Camera at index {camera_index} is working")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image")
                break
            cv2.imshow(f"Camera {camera_index}", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print(f"Cannot open camera at index {camera_index}")


if __name__ == "__main__":
    for i in range(5):  # Test camera indices from 0 to 4
        test_camera(i)
