import cv2
import numpy as np
import time
from PIL import Image

cap = cv2.VideoCapture(0)

# Cores no formato BGR
yellow = [0, 255, 255]
blue = [255, 0, 0]


def get_limits(color_name):
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

    return color_limits[color_name]


while True:
    ret, frame = cap.read()

    if ret:
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Deteccao objetos amarelos
        lower_yellow, upper_yellow = get_limits("yellow")
        mask_yellow = cv2.inRange(
            hsv_img, np.array(lower_yellow), np.array(upper_yellow)
        )
        _mask_yellow = Image.fromarray(mask_yellow)
        bbox_yellow = _mask_yellow.getbbox()

        # Deteccao objetos azuis
        lower_blue, upper_blue = get_limits("blue")
        mask_blue = cv2.inRange(hsv_img, np.array(lower_blue), np.array(upper_blue))
        _mask_blue = Image.fromarray(mask_blue)
        bbox_blue = _mask_blue.getbbox()

        # Deteccao objetos vermelhos
        lower_red1, upper_red1 = get_limits("red2")
        mask_red1 = cv2.inRange(hsv_img, np.array(lower_red1), np.array(upper_red1))
        _mask_red1 = Image.fromarray(mask_red1)
        bbox_red1 = _mask_red1.getbbox()

        cv2.imshow("frame", cv2.flip(frame, 1))

        if bbox_yellow is not None:
            x1, y1, x2, y2 = bbox_yellow
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

        if bbox_blue is not None:
            x1, y1, x2, y2 = bbox_blue
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)

        if bbox_red1 is not None:
            x1, y1, x2, y2 = bbox_red1
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)

        # Mostrar o frame com o retângulo desenhado
        cv2.imshow("frame_with_rectangle", cv2.flip(frame, 1))

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
