import cv2


def find_available_cameras():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
        if cap.isOpened():
            print(f"Camera found at index {index}")
            arr.append(index)
        else:
            break
        cap.release()
        index += 1
    if not arr:
        print("No cameras found")
    return arr


if __name__ == "__main__":
    find_available_cameras()
