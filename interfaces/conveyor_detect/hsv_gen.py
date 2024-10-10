import cv2
import numpy as np


def foo(x):
    pass


# Barra de rolagem
title = "Generator HSV"
cv2.namedWindow(title)
cv2.createTrackbar("Hue", title, 0, 179, foo)
cv2.createTrackbar("Saturation", title, 255, 255, foo)
cv2.createTrackbar("Value", title, 255, 255, foo)

img_hsv = np.zeros((255, 500, 3), np.uint8)

while True:
    h = cv2.getTrackbarPos("Hue", title)
    s = cv2.getTrackbarPos("Saturation", title)
    v = cv2.getTrackbarPos("Value", title)

    img_hsv[:] = (h, s, v)
    img_bgr = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

    cv2.imshow(title, img_bgr)

    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
