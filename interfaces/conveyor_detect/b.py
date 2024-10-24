import cv2
import serial
import numpy as np
from serial.tools import list_ports


class Detector:
    def __init__(self, camera=0, trigger=None, baudrate=9600, portCom="/dev/ttyACM0"):
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
            cap = cv2.VideoCapture(self.camera)
            while True:
                ret, frame = cap.read()

                if self.ser.in_waiting > 0:
                    self.my_trigger = self.ser.readline().decode().strip()
                    print(f"Trigger detectado! - {self.trigger}")

                    if self.trigger == "detectar":
                        # Intervalos de HSV - Hue, Saturation, Value
                        azul_min = np.array([100, 0, 50])
                        azul_max = np.array([130, 255, 255])

                        verde_min = np.array([50, 50, 50])
                        verde_max = np.array([80, 255, 255])

                        vermelho_min = np.array([0, 50, 50])
                        vermelho_max = np.array([10, 255, 255])

                        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                        # Deteccao das cores
                        mask_azul = cv2.inRange(frame_hsv, azul_min, azul_max)
                        mask_verde = cv2.inRange(frame_hsv, verde_min, verde_max)
                        mask_vermelho = cv2.inRange(
                            frame_hsv, vermelho_min, vermelho_max
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

                        # Desenhar retângulos ao redor das áreas detectadas
                        if contours_azul:
                            for cnt in contours_azul:
                                x, y, w, h = cv2.boundingRect(cnt)
                                cv2.rectangle(
                                    frame, (x, y), (x + w, y + h), (255, 0, 0), 2
                                )  # Retângulo azul
                            self.ser.write(b"azul\n")

                        if contours_verde:
                            for cnt in contours_verde:
                                x, y, w, h = cv2.boundingRect(cnt)
                                cv2.rectangle(
                                    frame, (x, y), (x + w, y + h), (0, 255, 0), 2
                                )  # Retângulo verde
                            self.ser.write(b"verde\n")

                        if contours_vermelho:
                            for cnt in contours_vermelho:
                                x, y, w, h = cv2.boundingRect(cnt)
                                cv2.rectangle(
                                    frame, (x, y), (x + w, y + h), (0, 0, 255), 2
                                )  # Retângulo vermelho
                            self.ser.write(b"vermelho\n")

                        if contours_azul or contours_verde or contours_vermelho:
                            cv2.imshow("Result:", frame)
                        if not (contours_azul or contours_verde or contours_vermelho):
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
    iport = str(input("Digite uma port valida: "))

    detector = Detector(camera=2, baudrate=9600, portCom=iport)
    detector.open_serial()
    detector.color_detector()
