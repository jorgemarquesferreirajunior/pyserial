from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import serial
import warnings

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

        # Combo boxes
        self.cb_serial_list = QComboBox()

        # Labels
        self.lb_camera_runtime = QLabel()
        self.lb_camera_detection = QLabel()
        self.lb_status_serial = QLabel()

        # Text Edit
        self.te_output = QTextEdit()

        # Spacers
        self.spacer_v = QSpacerItem(20, 20, QSizePolicy.Minimun, QSizePolicy.Expanding)
        self.spacer_h = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimun)

        """
        Display
        """

        self.lb_status_serial.setText("disconected")

        self.layout_serial.addWidget(self.btn_connect)
        self.layout_serial.addWidget(self.btn_disconnect)
        self.layout_serial.addWidget(self.lb_status_serial)

        self.layout_trailer.addWidget(self.cb_serial_list)
        self.layout_trailer.addLayout(self.layout_serial)
        self.layout_trailer.addSpacerItem(self.spacer_h)
        self.layout_trailer.addWidget(self.te_output)

        self.showMaximized()
        self.setWindowTitle("Conveyor Detection")
        self.setLayout(self.layout_main)


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
        self.ser.write(data)

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
