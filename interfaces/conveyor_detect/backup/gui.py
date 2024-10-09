import cv2
import util
import numpy as np
import threading
import time
from PIL import Image

cap = cv2.VideoCapture(0)
yellow = [0, 255, 255]  # formato BGR
blue = [255, 0, 0]
red = [0, 0, 255]
rect_size = 50
avg_rgb = np.array([])


def mostra_rgb():
    while True:
        if avg_rgb.size > 0:
            print(f"Valor médio RGB na área central: {avg_rgb}")
            print(f"Lower limit: {lower_limit}, Upper limit: {upper_limit}")
        time.sleep(1)


thr_mostra_rgb = threading.Thread(target=mostra_rgb)
thr_mostra_rgb.daemon = True
thr_mostra_rgb.start()

while True:
    ret, frame = cap.read()

    if ret:
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_limit, upper_limit = util.get_limits(color=yellow)

        mask = cv2.inRange(hsv_img, lower_limit, upper_limit)

        _mask = Image.fromarray(mask)

        bbox = _mask.getbbox()

        if bbox is not None:
            x1, y1, x2, y2 = bbox

            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

        """ lower_limits, upper_limits = util.get_limits_red()

        # Criar máscaras para cada intervalo de vermelho
        mask1 = cv2.inRange(hsv_img, lower_limits[0], upper_limits[0])
        mask2 = cv2.inRange(hsv_img, lower_limits[1], upper_limits[1])

        mask = cv2.bitwise_or(mask1, mask2) """

        cv2.imshow("frame", cv2.flip(frame, 1))
        # cv2.imshow("hsv", cv2.flip(hsv_img, 1))
        cv2.imshow("mask", cv2.flip(mask, 1))

        # Pegando o ponto central da imagem para exibir o valor RGB
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2  # Centro da imagem

        # Definir as coordenadas do retângulo ao redor do ponto central
        top_left_x = center_x - rect_size // 2
        top_left_y = center_y - rect_size // 2
        bottom_right_x = center_x + rect_size // 2
        bottom_right_y = center_y + rect_size // 2

        # Desenhar o retângulo verde ao redor do ponto central
        cv2.rectangle(
            frame,
            (top_left_x, top_left_y),
            (bottom_right_x, bottom_right_y),
            (0, 255, 0),
            2,
        )

        # Calcular a média de RGB na região do retângulo
        region = frame[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
        avg_bgr = np.mean(region, axis=(0, 1)).astype(int)  # Média BGR na região

        # Exibir o valor RGB (convertido de BGR)
        avg_rgb = avg_bgr[::-1]  # Inverte para RGB
        # print(f"Valor médio RGB na área central: {avg_rgb}")

        # Mostrar o frame com o retângulo desenhado
        cv2.imshow("frame_with_rectangle", cv2.flip(frame, 1))

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
