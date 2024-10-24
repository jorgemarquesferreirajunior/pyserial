import cv2
import numpy as np


# Função para detectar cor e desenhar retângulos
def detectar_cor(frame, roi, lower_bound, upper_bound, color_name, color_bgr):
    # Converter o frame de BGR para HSV
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Criar uma máscara para a cor desejada
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Encontrar contornos na região de interesse (ROI)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Desenhar contornos e retângulos ao redor das áreas detectadas na ROI
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:  # Filtrar pequenas áreas de ruído
            x, y, w, h = cv2.boundingRect(contour)
            # Ajustar as coordenadas do retângulo para a imagem original
            cv2.rectangle(
                frame,
                (x + roi_x, y + roi_y),
                (x + roi_x + w, y + roi_y + h),
                color_bgr,
                2,
            )
            cv2.putText(
                frame,
                color_name,
                (x + roi_x, y + roi_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color_bgr,
                2,
            )


# Inicializar a captura de vídeo
cap = cv2.VideoCapture("http://10.202.0.220:8080/video")

# Faixas de cores HSV para o arco-íris
cores = {
    "Vermelho": [(0, 100, 100), (10, 255, 255), (0, 0, 255)],
    "Laranja": [(11, 100, 100), (25, 255, 255), (0, 165, 255)],
    "Amarelo": [(26, 85, 255), (39, 186, 255), (0, 255, 255)],
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
    # frame = cv2.flip(frame, 1)

    if not ret:
        break

    # Ignorar o fundo laranja, criando uma máscara
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    fundo_mascara = cv2.inRange(hsv, lower_orange, upper_orange)
    frame[fundo_mascara > 0] = (0, 0, 0)  # Definir o fundo laranja como preto

    # Definir a região de interesse (ROI) de 50x50 pixels no centro da imagem
    height, width, _ = frame.shape
    roi_x = width // 2 - 25
    roi_y = height // 2 - 25
    roi = frame[roi_y : roi_y + 50, roi_x : roi_x + 50]  # ROI de 50x50 pixels

    # Desenhar um retângulo ao redor da ROI no frame principal (opcional, para visualização)
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x + 50, roi_y + 50), (255, 255, 255), 2)

    # Detectar cada cor do arco-íris dentro da ROI
    for nome_cor, (lower, upper, cor_bgr) in cores.items():
        detectar_cor(frame, roi, np.array(lower), np.array(upper), nome_cor, cor_bgr)

    # Mostrar o frame com as cores detectadas
    cv2.imshow("Detecção de Cores - Arco-íris na ROI", frame)

    # Pressionar 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Liberar a captura de vídeo e fechar as janelas
cap.release()
cv2.destroyAllWindows()
