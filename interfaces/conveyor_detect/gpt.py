import cv2
import numpy as np
import time
from PIL import Image

cap = cv2.VideoCapture(0)
yellow = [0, 255, 255]  # formato BGR
blue = [255, 0, 0]  # formato BGR
red = [0, 0, 255]  # formato BGR
rect_size = 50
avg_rgb = np.array([])


def get_limits(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lower_limit = (hsvC[0][0][0] - 10, 100, 100)
    upper_limit = (hsvC[0][0][0] + 10, 255, 255)

    lower_limit = np.array(lower_limit, dtype=np.uint8)
    upper_limit = np.array(upper_limit, dtype=np.uint8)

    return lower_limit, upper_limit


def get_limits_blue():
    # Limites para a cor azul
    lower_limit = np.array([100, 100, 100], dtype=np.uint8)
    upper_limit = np.array([140, 255, 255], dtype=np.uint8)
    return lower_limit, upper_limit


while True:
    ret, frame = cap.read()

    if ret:
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Máscara para a cor amarela
        lower_limit_yellow, upper_limit_yellow = get_limits(color=yellow)
        mask_yellow = cv2.inRange(hsv_img, lower_limit_yellow, upper_limit_yellow)

        # Máscara para a cor azul
        lower_limit_blue, upper_limit_blue = get_limits_blue()
        mask_blue = cv2.inRange(hsv_img, lower_limit_blue, upper_limit_blue)

        # Combinar as máscaras
        combined_mask = cv2.bitwise_or(mask_yellow, mask_blue)

        # Encontrar contornos
        contours, _ = cv2.findContours(
            combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Filtrar pequenos contornos
                x, y, w, h = cv2.boundingRect(contour)

                # Verificar a cor do contorno e desenhar o retângulo correspondente
                if mask_yellow[y : y + h, x : x + w].any():
                    color = (0, 255, 0)  # Verde para amarelo
                elif mask_blue[y : y + h, x : x + w].any():
                    color = (255, 0, 0)  # Azul para azul
                else:
                    continue

                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)

        # Mostrar o frame com os retângulos desenhados
        cv2.imshow("frame_with_rectangle", cv2.flip(frame, 1))

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
