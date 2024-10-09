from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import serial
from serial.tools import list_ports
import warnings
import time
import numpy as np
from PIL import Image

warnings.filterwarnings("ignore", category=DeprecationWarning)


class MainWin(QWidget):
    def __init__(self):
        super(MainWin, self).__init__()
        self.serial_connection = None

        """
        Widgets
        """

        # Layouts
        self.layout_main = QVBoxLayout()
        self.layout_serial = QVBoxLayout()
        self.layout_header = QHBoxLayout()
        self.layout_central = QHBoxLayout()
        self.layout_trailer = QHBoxLayout()

        # Buttons
        self.btn_connect = QPushButton("Connect")
        self.btn_disconnect = QPushButton("Disconnect")
        self.btn_search = QPushButton("Search")

        # List Widgets
        self.lw_serial_list = QListWidget()

        # Labels
        self.lb_camera_runtime = QLabel()
        self.lb_camera_detection = QLabel()
        self.lb_status_serial = QLabel()
        self.lb_watch = QLabel()

        # Timer
        self.timer = QTimer()

        # Text Edit
        self.te_output = QTextEdit()

        # Spacers
        self.spacer_v = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.spacer_h = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # QThreads

        self.worker = VideoWorker()
        self.worker.start()
        self.worker.image_update_runtime.connect(self.image_update_camera_runtime)
        self.worker.image_update_detection.connect(self.image_update_camera_detection)

        """
        Display
        """
        # Configurar as labels para redimensionamento automático
        self.lb_camera_runtime.setScaledContents(True)
        self.lb_camera_detection.setScaledContents(True)

        # Definir políticas de tamanho
        self.lb_camera_runtime.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.lb_camera_detection.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.lb_status_serial.setText("disconnected")
        self.timer.timeout.connect(self.update_watch)
        self.timer.start(1000)
        self.lb_camera_runtime.setText("Video 1")
        self.lb_camera_runtime.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.lb_camera_detection.setText("Video 2")
        self.lb_camera_detection.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.layout_serial.addWidget(self.btn_search)
        self.layout_serial.addWidget(self.btn_connect)
        self.layout_serial.addWidget(self.btn_disconnect)
        self.layout_serial.addWidget(self.lb_status_serial)

        self.layout_trailer.addWidget(self.lw_serial_list)
        self.layout_trailer.addLayout(self.layout_serial)
        self.layout_trailer.addSpacerItem(self.spacer_h)
        self.layout_trailer.addWidget(self.te_output)

        self.layout_central.addWidget(self.lb_camera_runtime)
        self.layout_central.addWidget(self.lb_camera_detection)

        self.layout_header.addSpacerItem(self.spacer_h)
        self.layout_header.addWidget(self.lb_watch)

        self.layout_main.addLayout(self.layout_header, 10)
        self.layout_main.addLayout(self.layout_central, 80)
        # self.layout_central.addSpacerItem(self.spacer_v)
        self.layout_main.addLayout(self.layout_trailer, 10)

        # Connecting button signals to the corresponding methods
        self.btn_search.clicked.connect(self.search_ports)
        self.btn_connect.clicked.connect(self.connect_serial)
        self.btn_disconnect.clicked.connect(self.disconnect_serial)

        self.showMaximized()
        self.setWindowTitle("Conveyor Detection")
        self.setLayout(self.layout_main)

        # Connections
        self.btn_search.clicked.connect(self.search_ports)

    def image_update_camera_runtime(self, image):
        """



        scaled_image = image.scaled(
            self.lb_camera_runtime.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.lb_camera_runtime.setPixmap(QPixmap.fromImage(scaled_image))"""
        # Calcular o tamanho máximo mantendo a proporção
        max_width = self.lb_camera_runtime.width()
        max_height = self.lb_camera_runtime.height()

        # Definir a nova largura e altura respeitando a proporção
        scaled_image = image.scaled(
            min(max_width, 640),
            min(max_height, 480),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.lb_camera_runtime.setPixmap(QPixmap.fromImage(scaled_image))

    def image_update_camera_detection(self, image):
        """

        scaled_image = image.scaled(
            self.lb_camera_detection.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.lb_camera_detection.setPixmap(QPixmap.fromImage(scaled_image))
        """
        # Calcular o tamanho máximo mantendo a proporção
        max_width = self.lb_camera_detection.width()
        max_height = self.lb_camera_detection.height()

        # Definir a nova largura e altura respeitando a proporção
        scaled_image = image.scaled(
            min(max_width, 640),
            min(max_height, 480),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.lb_camera_detection.setPixmap(QPixmap.fromImage(scaled_image))

    def update_watch(self):
        current_time = time.strftime("%H:%M:%S")
        self.lb_watch.setText(current_time)

    def search_ports(self):
        ports = list_ports.comports()

        self.lw_serial_list.clear()

        [
            self.lw_serial_list.addItem(str(port).strip().split(" ")[0])
            for port in ports
            if "n/a" not in port
        ]

    def connect_serial(self):
        try:
            port = self.lw_serial_list.currentItem().text()
            self.serial_connection = MySerial(port=port)
            if self.serial_connection.is_open:
                self.btn_connect.setStyleSheet("background-color: (0,255,0);")
        except Exception as e:
            self.te_output.append(f"Error: {str(e)}")

    def disconnect_serial(self):
        if self.serial_connection:
            self.serial_connection.ser.close()
            if not self.serial_connection.is_open:
                self.btn_connect.setStyleSheet("background-color: (255,0,0);")


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


class VideoWorker(QThread):
    image_update_runtime = pyqtSignal(QImage)
    image_update_detection = pyqtSignal(QImage)

    def run(self):
        capture = cv2.VideoCapture(0)
        self.thread_on = True

        while self.thread_on:
            ret, frame = capture.read()

            if ret:
                # Update runtime display
                image_runtime = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_runtime = cv2.flip(image_runtime, 1)
                image_pyqt_runtime = QImage(
                    image_runtime.data,
                    image_runtime.shape[1],
                    image_runtime.shape[0],
                    QImage.Format_RGB888,
                )
                pic_runtime = image_pyqt_runtime.scaled(640, 480, Qt.KeepAspectRatio)
                self.image_update_runtime.emit(pic_runtime)

                # Object detection logic
                hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                lower_yellow, upper_yellow = get_limits("yellow")
                mask_yellow = cv2.inRange(
                    hsv_img, np.array(lower_yellow), np.array(upper_yellow)
                )
                bbox_yellow = Image.fromarray(mask_yellow).getbbox()

                lower_blue, upper_blue = get_limits("blue")
                mask_blue = cv2.inRange(
                    hsv_img, np.array(lower_blue), np.array(upper_blue)
                )
                bbox_blue = Image.fromarray(mask_blue).getbbox()

                if bbox_yellow is not None:
                    x1, y1, x2, y2 = bbox_yellow
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

                if bbox_blue is not None:
                    x1, y1, x2, y2 = bbox_blue
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)

                # Update detection display
                image_detection = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_detection = cv2.flip(image_detection, 1)
                image_pyqt_detection = QImage(
                    image_detection.data,
                    image_detection.shape[1],
                    image_detection.shape[0],
                    QImage.Format_RGB888,
                )
                pic_detection = image_pyqt_detection.scaled(
                    640, 480, Qt.KeepAspectRatio
                )
                self.image_update_detection.emit(pic_detection)

    def stop(self):
        self.thread_on = False
        self.quit()


class MySerial:
    def __init__(self, port="COM1", baudrate="9600", parity="N", stopbits=1) -> None:
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.ser = serial.Serial(
            port=port, baudrate=baudrate, parity=parity, stopbits=stopbits
        )

    def send(self, data):
        self.ser.write(data.encode())

    def response(self):
        self.ser.timeout = 1
        response = self.ser.read_until(b"\n")
        while self.ser.in_waiting > 0:
            response += self.ser.read_until(b"\n")
        return response.decode("utf-8").splitlines()


if __name__ == "__main__":
    app = QApplication([])

    win = MainWin()
    win.show()

    app.exec()
