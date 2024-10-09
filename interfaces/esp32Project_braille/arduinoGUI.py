from time import sleep
from PyQt5.QtWidgets import (
    QApplication,
    QTextEdit,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QListWidget,
    QMessageBox,
    QCheckBox,
)

from PyQt5.QtCore import Qt
import serial
from serial.tools import list_ports
import warnings
from serial import Serial
from crcmod.predefined import mkPredefinedCrcFun
import struct
import ctypes
import crcmod

warnings.filterwarnings("ignore", category=DeprecationWarning)
crc16_xmodem = crcmod.predefined.Crc("xmodem")


class ArduinoGUISerial(QWidget):
    def __init__(self):
        super().__init__()

        self.my_serial = None

        # nicknames
        _btn_search = "Search"
        _btn_connect = "Connect"
        _btn_execute = "Execute"
        _btn_clear = "Clear"
        _label_serial_protocol = "Padrao Serial"
        _label_baudrate = "Baudrate"
        _label_command = "Command"
        _label_pc = "Pc"
        _label_device = "Device"
        _protocols = ["SERIAL_8N1", "SERIAL_8N2"]
        _baudrates = ["9600", "115200"]
        self._send_functions = ["translate", "execute prog", "change speed", ""]
        self._request_functions = ["get speed", ""]
        _label_address = "Address"

        """
        Widgets
        """
        # Buttons
        self.btn_search = QPushButton(_btn_search)
        self.btn_connect = QPushButton(_btn_connect)
        self.btn_clear = QPushButton(_btn_clear)
        self.btn_execute = QPushButton(_btn_execute)
        # ListWidget
        self.port_list = QListWidget()
        self.view_pc_chat = QListWidget()
        self.view_device_chat = QListWidget()
        # Labels
        self.label_serial_protocol = QLabel(_label_serial_protocol)
        self.label_baudrate = QLabel(_label_baudrate)
        self.label_command = QLabel(_label_command)
        self.label_pc = QLabel(_label_pc)
        self.label_device = QLabel(_label_device)
        self.label_send_request = QLabel()
        self.label_address = QLabel(_label_address)

        # ComboBox
        self.cb_serial_protocol = QComboBox()
        self.cb_baudrate = QComboBox()
        self.cb_functions = QComboBox()

        # LineEdit
        self.le_command = QLineEdit()
        self.le_address = QLineEdit()
        self.le_translate_text = QLineEdit()

        # TextEdit
        self.te_translate_text = QTextEdit()

        # CheckBox
        self.ck_send_request = QCheckBox()

        # Spacers
        self.horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )
        self.vertical_spacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        """
        Layouts
        """
        self.main_layout = QHBoxLayout()
        self.lateral_layout = QVBoxLayout()
        self.serial_layout = QVBoxLayout()
        self.baudrate_layout = QVBoxLayout()
        self.central_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.command_layout = QVBoxLayout()
        self.execute_clear_layout = QVBoxLayout()
        self.chat_layout = QHBoxLayout()
        self.pc_layout = QVBoxLayout()
        self.device_layout = QVBoxLayout()
        self.send_request_layout = QVBoxLayout()
        self.address_layout = QVBoxLayout()

        """
        App Design
        """
        # lateral_layout design
        self.cb_serial_protocol.addItems(_protocols)
        self.cb_baudrate.addItems(_baudrates)
        self.serial_layout.addWidget(self.label_serial_protocol)
        self.serial_layout.addWidget(self.cb_serial_protocol)
        self.baudrate_layout.addWidget(self.label_baudrate)
        self.baudrate_layout.addWidget(self.cb_baudrate)
        self.lateral_layout.addWidget(self.btn_search)
        self.lateral_layout.addWidget(self.port_list)
        self.lateral_layout.addLayout(self.serial_layout)
        self.lateral_layout.addLayout(self.baudrate_layout)
        self.lateral_layout.addWidget(self.btn_connect)
        self.main_layout.addLayout(self.lateral_layout, 20)

        # central_layout design
        self.le_address.setFixedWidth(150)
        self.le_address.setMaxLength(1)
        self.address_layout.addWidget(self.label_address)
        self.address_layout.addWidget(self.le_address)
        self.cb_functions.clear()
        self.cb_functions.addItems(self._send_functions)
        self.cb_functions.setMaximumWidth(150)
        self.ck_send_request.setText("Send")
        self.ck_send_request.setChecked(False)
        self.ck_send_request.setMinimumWidth(100)
        self.ck_send_request.setMaximumWidth(150)
        self.send_request_layout.addWidget(self.ck_send_request)
        self.send_request_layout.addWidget(self.cb_functions)
        self.btn_clear.setMaximumWidth(150)
        self.btn_execute.setMaximumWidth(150)
        self.execute_clear_layout.addWidget(self.btn_clear)
        self.execute_clear_layout.addWidget(self.btn_execute)
        self.le_translate_text.setMinimumWidth(300)
        self.le_translate_text.setMinimumHeight(60)
        self.te_translate_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.te_translate_text.setMaximumHeight(50)
        self.te_translate_text.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred
        )

        self.top_layout.addLayout(self.address_layout)
        self.top_layout.addLayout(self.send_request_layout)
        self.top_layout.addLayout(self.execute_clear_layout)
        self.top_layout.addWidget(self.te_translate_text)
        # self.top_layout.addItem(self.horizontal_spacer)
        self.pc_layout.addWidget(self.label_pc)
        self.pc_layout.addWidget(self.view_pc_chat)
        self.device_layout.addWidget(self.label_device)
        self.device_layout.addWidget(self.view_device_chat)
        self.chat_layout.addLayout(self.pc_layout)
        self.chat_layout.addLayout(self.device_layout)
        self.central_layout.addLayout(self.top_layout)
        self.central_layout.addLayout(self.chat_layout)
        # main_layout design
        self.main_layout.addLayout(self.central_layout, 80)
        self.setLayout(self.main_layout)
        self.setWindowTitle("Arduino Serial - RS485")
        self.showMaximized()

        # Connections
        self.btn_search.clicked.connect(self.update_port_list)
        self.btn_connect.clicked.connect(self.create_serial)
        self.btn_execute.clicked.connect(self.execute_prog)
        self.btn_clear.clicked.connect(self.clear_chat)
        self.ck_send_request.stateChanged.connect(self.update_ck_send_request)

    # Methods
    def update_port_list(self):
        ports = list_ports.comports()
        self.port_list.clear()

        [
            self.port_list.addItem(str(port).strip().split(" ")[0])
            for port in ports
            if "n/a" not in port
        ]

    def create_serial(self):
        try:
            self.my_serial = MySerial(
                port=self.port_list.currentItem().text(),
                baudrate=int(self.cb_baudrate.currentText()),
                parity="N",
                stopbits=int(self.cb_serial_protocol.currentText()[-1]),
            )

            if self.my_serial.serial.is_open:
                self.btn_connect.setStyleSheet("background-color: rgb(0,255,0);")
            else:
                raise Exception("ERROR: Serial not opened !")
        except Exception as e:
            self.my_serial = None
            print(f"Error to create Serial COM : {e}")
            self.btn_connect.setStyleSheet("background-color: rgb(255,0,0);")

    def update_pc_chat(self, command):
        self.view_pc_chat.addItem(f"Request: {command}")

    def update_device_chat(self, command):
        self.view_device_chat.addItem(f"Response: {command}")

    def execute_prog(self):
        send = not self.ck_send_request.isChecked()
        address = str(self.le_address.text()).strip().upper()
        func = self.cb_functions.currentText()[0].upper()
        data = self.te_translate_text.toPlainText()[:51].lower()
        if len(data) == 0:
            data = " "
        len_data = str(len(data)).zfill(2)

        message = address + func + len_data + data

        print(f"Frame created: {message}")

        crc16_val = crc16_xmodem.new(message.encode()).crcValue
        message += str(crc16_val) + "\n"

        self.my_serial.send_frame(frame=message.encode())
        # sleep(0.2)
        self.te_translate_text.clear()

        response = self.my_serial.response_frame()
        if not response:
            response = ["ERROR"]

        print(f"crc calculated: {crc16_val} : {hex(crc16_val)}")
        print(f"Frame sent: {message}")
        print(f"Response: ")
        [print(data) for data in response]

        self.view_pc_chat.addItem(
            f"PC: [addres, func, len_data, data, crc] = {address},{func},{len_data},{data},{str(crc16_val)}"
        )
        self.view_device_chat.addItem(f"Device: {response[0]}")

        # campo de endereco preenchido
        if address != "":
            pass
        else:
            print("Address not configured")

    def clear_chat(self):
        self.view_device_chat.clear()
        self.view_pc_chat.clear()

    def update_ck_send_request(self, _):
        self.cb_functions.clear()

        if self.ck_send_request.isChecked():
            self.cb_functions.addItems(self._request_functions)
            self.ck_send_request.setText("Request")
            # self.ck_send_request.setStyleSheet("QCheckBox { background-color: rgba(40,240,40,150);}")
            self.ck_send_request.setStyleSheet("QCheckBox { font-style: italic;}")
            self.te_translate_text.hide()
            self.top_layout.addItem(self.horizontal_spacer)
        else:
            self.cb_functions.addItems(self._send_functions)
            self.ck_send_request.setText("Send")
            self.ck_send_request.setStyleSheet("QCheckBox { font-style: normal;}")
            self.top_layout.removeItem(self.horizontal_spacer)
            self.te_translate_text.setSizePolicy(
                QSizePolicy.Expanding, QSizePolicy.Preferred
            )
            self.te_translate_text.show()
            # self.ck_send_request.setStyleSheet("QCheckBox { background-color: rgba(40,40,240,150);}")


class MySerial:
    def __init__(self, port="COM1", baudrate=9600, parity="N", stopbits=1) -> None:
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.serial = Serial(
            port=port, baudrate=baudrate, parity=parity, stopbits=stopbits
        )

    def send_frame(self, frame):
        # self.serial.reset_input_buffer()
        # self.serial.reset_output_buffer()

        self.serial.write(frame)

    def response_frame(self):
        self.serial.timeout = 1
        response = self.serial.read_until(b"\n")

        while self.serial.in_waiting > 0:
            response += self.serial.read_until(b"\n")
        return response.decode("utf-8").splitlines()

    def create_frame(self, addres, function, data):
        pass


if __name__ == "__main__":
    app = QApplication([])
    win = ArduinoGUISerial()
    win.show()
    app.exec()
