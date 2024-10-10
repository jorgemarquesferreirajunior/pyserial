import cv2
import numpy as np
import time
from PIL import Image

cap = cv2.VideoCapture(0)

# Cores no formato BGR
yellow = [0, 255, 255]
blue = [255, 0, 0]
red = [0, 0, 255]


def get_limits(color, color_name):
    color_limits = {
        "yellow": ([20, 100, 100], [30, 255, 255]),
        "blue": ([100, 100, 100], [140, 255, 255]),
        "green": ([40, 100, 100], [80, 255, 255]),
        "red1": ([0, 100, 100], [10, 255, 255]),
        "red2": ([170, 100, 100], [180, 255, 255]),
        "orange": ([10, 100, 100], [20, 255, 255]),
        "purple": ([140, 100, 100], [160, 255, 255]),
        "pink": ([160, 100, 100], [180, 255, 255]),
        "cyan": ([80, 100, 100], [100, 255, 255]),
        "black": ([0, 0, 0], [180, 255, 30]),
        "white": ([0, 0, 200], [180, 20, 255]),
        "gray": ([0, 0, 50], [180, 25, 200]),
    }

    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lower_limit = (
        hsvC[0][0][0] - color_limits[color_name][0][0],
        color_limits[color_name][0][1],
        color_limits[color_name][0][2],
    )
    upper_limit = (
        hsvC[0][0][0] - color_limits[color_name][1][0],
        color_limits[color_name][1][1],
        color_limits[color_name][1][2],
    )

    lower_limit = np.array(lower_limit, dtype=np.uint8)
    upper_limit = np.array(upper_limit, dtype=np.uint8)

    return lower_limit, upper_limit


while True:
    ret, frame = cap.read()

    if ret:
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Deteccao objetos amarelos
        lower_yellow, upper_yellow = get_limits(color=yellow, color_name="yellow")
        mask_yellow = cv2.inRange(hsv_img, lower_yellow, upper_yellow)
        _mask_yellow = Image.fromarray(mask_yellow)
        bbox_yellow = _mask_yellow.getbbox()

        # Deteccao objetos azuis
        lower_blue, upper_blue = get_limits(color=blue, color_name="blue")
        mask_blue = cv2.inRange(hsv_img, lower_blue, upper_blue)
        _mask_blue = Image.fromarray(mask_blue)
        bbox_blue = _mask_blue.getbbox()

        cv2.imshow("frame", cv2.flip(frame, 1))

        if bbox_yellow is not None:
            x1, y1, x2, y2 = bbox_yellow
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        if bbox_blue is not None:
            x1, y1, x2, y2 = bbox_blue
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)

        # Mostrar o frame com o retângulo desenhado
        cv2.imshow("frame_with_rectangle", cv2.flip(frame, 1))

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
