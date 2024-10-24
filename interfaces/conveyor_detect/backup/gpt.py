import cv2
import numpy as np


# Função para detectar cor e desenhar retângulos
def detectar_cor(frame, lower_bound, upper_bound, color_name, color_bgr):
    # Converter o frame de BGR para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Criar uma máscara para a cor desejada
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Encontrar contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Desenhar contornos e retângulos ao redor das áreas detectadas
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:  # Filtrar pequenas áreas de ruído
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color_bgr, 2)
            cv2.putText(
                frame,
                color_name,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color_bgr,
                2,
            )


# Inicializar a captura de vídeo
cap = cv2.VideoCapture("http://10.202.0.220:8080/video")

# Faixas de cores HSV para o arco-íris
cores = {
    "Vermelho": [(0, 100, 255), (6, 255, 255), (0, 0, 255)],
    "Laranja": [(11, 100, 100), (25, 255, 255), (0, 165, 255)],
    "Amarelo": [(26, 85, 100), (35, 255, 255), (0, 255, 255)],
    "Verde": [(36, 100, 100), (85, 255, 255), (0, 255, 0)],
    "Azul": [(86, 100, 100), (125, 255, 255), (255, 0, 0)],
    "Anil": [(126, 100, 100), (145, 255, 255), (130, 0, 75)],
    "Violeta": [(146, 100, 100), (160, 255, 255), (255, 0, 255)],
}

# Faixa de cor laranja para o fundo
lower_orange = np.array([11, 100, 100])
upper_orange = np.array([25, 255, 255])

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Ignorar o fundo laranja, criando uma máscara
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    fundo_mascara = cv2.inRange(hsv, lower_orange, upper_orange)
    frame[fundo_mascara > 0] = (0, 0, 0)  # Definir o fundo laranja como preto

    # Detectar cada cor do arco-íris
    for nome_cor, (lower, upper, cor_bgr) in cores.items():
        detectar_cor(frame, np.array(lower), np.array(upper), nome_cor, cor_bgr)

    # Mostrar o frame com as cores detectadas
    print(frame.shape)
    cv2.imshow("Detecção de Cores - Arco-íris", frame)

    # Pressionar 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Liberar a captura de vídeo e fechar as janelas
cap.release()
cv2.destroyAllWindows()
