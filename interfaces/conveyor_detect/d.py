import cv2
import serial
import numpy as np
from serial.tools import list_ports
from time import sleep


class Detector:
    def __init__(self, camera=2, trigger=None, baudrate=9600, portCom="/dev/ttyACM0"):
        self.camera = camera
        self.trigger = trigger
        self.ser = None
        self.baudrate = baudrate
        self.port = portCom

    @property
    def my_port(self):
        return self.port

    @my_port.setter
    def my_port(self, value):
        self.port = value

    @property
    def my_camera(self):
        return self.camera

    @my_camera.setter
    def my_camera(self, value):
        self.camera = value

    @property
    def my_baudrate(self):
        return self.baudrate

    @my_baudrate.setter
    def my_baudrate(self, value):
        self.baudrate = value

    @property
    def my_trigger(self):
        return self.trigger

    @my_trigger.setter
    def my_trigger(self, value):
        self.trigger = value

    def open_serial(self):
        try:
            self.ser = serial.Serial(port=self.port, baudrate=self.baudrate)
            print(f"Connected to port: {self.port}")
        except Exception as e:
            print(f"Port not opened: {e}")

    def color_detector(self):
        if self.ser:
            cap = cv2.VideoCapture(self.camera, cv2.CAP_V4L2)
            msg = ""
            cont = 0
            while True:
                resp_azul, resp_verde, resp_vermelho = None, None, None
                show_msg = False
                ret, frame = cap.read()
                height, width, _ = frame.shape

                # Definindo o centro da imagem
                centro_x, centro_y = width // 2, height // 2

                # Dimensões da região de interesse (50x50)
                roi_size = 50
                x1 = centro_x - roi_size // 2
                y1 = centro_y - roi_size // 2
                x2 = x1 + roi_size
                y2 = y1 + roi_size

                # Desenhar o retângulo preto ao redor da região de interesse (ROI)
                cv2.rectangle(
                    frame, (x1 - 10, y1 - 10), (x2 + 10, y2 + 10), (0, 0, 0), 2
                )

                # Foco na região central (ROI)
                roi = frame[y1:y2, x1:x2]

                if self.ser.in_waiting > 0:
                    self.my_trigger = self.ser.readline().decode().strip()
                    print(f"Trigger detectado! - {self.trigger}", end=" ")

                    if self.trigger == "detectar":
                        # Intervalos de HSV - Hue, Saturation, Value
                        azul_min = np.array([105, 0, 50])
                        azul_max = np.array([127, 255, 255])

                        verde_min = np.array([50, 50, 50])
                        verde_max = np.array([100, 255, 255])

                        vermelho_min = np.array([0, 50, 50])
                        vermelho_max = np.array([10, 255, 255])

                        vermelho2_min = np.array([160, 50, 50])
                        vermelho2_max = np.array([180, 255, 255])

                        roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

                        # Exibir os valores de hue, saturation, e value no centro da ROI
                        centro_roi_x, centro_roi_y = (
                            roi.shape[1] // 2,
                            roi.shape[0] // 2,
                        )
                        hue, saturation, value = roi_hsv[centro_roi_y, centro_roi_x]
                        print(
                            f" - Hue: {hue}, Saturation: {saturation}, Value: {value}",
                            end=" - ",
                        )

                        # Detecção das cores na ROI
                        mask_azul = cv2.inRange(roi_hsv, azul_min, azul_max)
                        mask_verde = cv2.inRange(roi_hsv, verde_min, verde_max)
                        mask_vermelho = cv2.inRange(roi_hsv, vermelho_min, vermelho_max)
                        mask_vermelho2 = cv2.inRange(
                            roi_hsv, vermelho2_min, vermelho2_max
                        )

                        # Encontrar contornos para cada cor
                        contours_azul, _ = cv2.findContours(
                            mask_azul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                        )
                        contours_verde, _ = cv2.findContours(
                            mask_verde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                        )
                        contours_vermelho, _ = cv2.findContours(
                            mask_vermelho, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                        )

                        contours_vermelho2, _ = cv2.findContours(
                            mask_vermelho2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                        )

                        # Define o tamanho mínimo de área do contorno
                        tamanho_minimo_contorno = 100

                        # Desenhar retângulos ao redor das áreas detectadas na ROI
                        if (
                            not contours_azul
                            and not contours_vermelho
                            and not contours_verde
                            and not contours_vermelho2
                        ):
                            print("Nada encontrado")
                        if contours_azul:
                            resp_azul = True
                            resp_verde = True
                            resp_vermelho = False
                            print("Azul detectado")
                            for cnt in contours_azul:
                                area = cv2.contourArea(cnt)
                                if area > tamanho_minimo_contorno:
                                    x, y, w, h = cv2.boundingRect(cnt)
                                    cv2.rectangle(
                                        roi, (x, y), (x + w, y + h), (255, 0, 0), 2
                                    )
                            self.ser.write(b"azul\n")

                        if contours_verde:
                            resp_azul = False
                            resp_verde = True
                            resp_vermelho = False
                            print("Verde detectado")
                            for cnt in contours_verde:
                                area = cv2.contourArea(cnt)
                                if area > tamanho_minimo_contorno:
                                    x, y, w, h = cv2.boundingRect(cnt)
                                    cv2.rectangle(
                                        roi, (x, y), (x + w, y + h), (0, 255, 0), 2
                                    )
                            self.ser.write(b"verde\n")

                        if contours_vermelho or contours_vermelho2:
                            resp_azul = False
                            resp_verde = False
                            resp_vermelho = True
                            print("Vermelho detectado")
                            for cnt in contours_vermelho:
                                area = cv2.contourArea(cnt)
                                if area > tamanho_minimo_contorno:
                                    x, y, w, h = cv2.boundingRect(cnt)
                                    cv2.rectangle(
                                        roi, (x, y), (x + w, y + h), (0, 0, 255), 2
                                    )
                            self.ser.write(b"vermelho\n")

                            # if contours_azul or contours_verde or contours_vermelho:
                            # cv2.imshow("Result:", frame)
                        if contours_azul or contours_verde or contours_vermelho:
                            cont += 1
                            data = f"\ndeteccao {cont} - "
                            if contours_azul:
                                data += "azul"
                            elif contours_verde:
                                data += "verde"
                            elif contours_vermelho:
                                data += "vermelho"

                            msg += data
                            frame = cv2.putText(
                                frame,
                                msg,
                                (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (255, 0, 0),
                                2,
                            )
                        if not (contours_azul or contours_verde or contours_vermelho):
                            resp_azul = False
                            resp_verde = False
                            resp_vermelho = False
                            self.ser.write(b"nada\n")

                cv2.imshow("COLOR-DETECT", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            self.ser.close()
            cap.release()
            cv2.destroyAllWindows()
        else:
            print("Serial port not configured")


def find_ports():
    ports = list_ports.comports()
    av_ports = [port.description for port in ports if "n/a" not in port]
    if av_ports:
        [print(port) for port in av_ports]
    else:
        print("0 Ports found")


if __name__ == "__main__":
    # Exemplo de uso
    find_ports()
    # iport = str(input("Digite uma port valida: "))

    detector = Detector(camera=2, baudrate=9600, portCom="/dev/ttyACM0")
    detector.open_serial()
    detector.color_detector()
