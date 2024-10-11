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
        _btn_close_serial = "Disconnect"
        _label_serial_protocol = "Padrao Serial"
        _label_baudrate = "Baudrate"
        _label_command = "Command"
        _label_pc = "Pc"
        _label_device = "Device"
        _protocols = ["SERIAL_8N1", "SERIAL_8N2"]
        _baudrates = ["9600", "115200"]
        self._send_functions = ["translate", "execute prog", "change speed", ""]
        self._request_functions = ["get speed", "get message", ""]
        _label_address = "Address"

        """
        Widgets
        """
        # Buttons
        self.btn_search = QPushButton(_btn_search)
        self.btn_connect = QPushButton(_btn_connect)
        self.btn_clear = QPushButton(_btn_clear)
        self.btn_execute = QPushButton(_btn_execute)
        self.btn_close_serial = QPushButton(_btn_close_serial)
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
        self.lateral_layout.addWidget(self.btn_close_serial)
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
        self.btn_close_serial.clicked.connect(self.close_serial)
        self.ck_send_request.stateChanged.connect(self.update_ck_send_request)

    # Methods
    def update_port_list(self):
        ports = list_ports.comports()  # Obtém a lista de portas seriais disponíveis
        self.port_list.clear()  # Limpa a lista de portas

        # Adiciona cada porta serial disponível à lista, ignorando portas "n/a"
        [
            self.port_list.addItem(str(port).strip().split(" ")[0])
            for port in ports
            if "n/a" not in port
        ]

    def create_serial(self):
        try:
            # Cria uma instância de MySerial com as configurações escolhidas pelo usuário
            self.my_serial = MySerial(
                port=self.port_list.currentItem().text(),  # Porta selecionada na lista
                baudrate=int(self.cb_baudrate.currentText()),  # Baudrate selecionado
                parity="N",  # Paridade "N" (Nenhuma)
                stopbits=int(
                    self.cb_serial_protocol.currentText()[-1]
                ),  # Bits de parada
            )

            # Se a serial foi aberta com sucesso, muda a cor do botão de conexão para verde
            if self.my_serial.serial.is_open:
                self.btn_connect.setStyleSheet("background-color: rgb(0,255,0);")
            else:
                raise Exception(
                    "ERROR: Serial not opened !"
                )  # Gera exceção se a serial não abrir
        except Exception as e:
            # Em caso de erro, exibe a mensagem de erro e muda a cor do botão para vermelho
            self.my_serial = None
            print(f"Error to create Serial COM : {e}")
            self.btn_connect.setStyleSheet("background-color: rgb(255,0,0);")

    def close_serial(self):
        # Fecha a conexão serial se estiver aberta e muda o botão de conexão para vermelho
        if self.my_serial.serial.is_open:
            self.my_serial.serial.close()
            self.btn_connect.setStyleSheet("background-color: rgb(255,0,0);")

    def update_pc_chat(self, command):
        # Atualiza o chat do PC com o comando enviado
        self.view_pc_chat.addItem(f"Request: {command}")

    def update_device_chat(self, command):
        # Atualiza o chat do dispositivo com a resposta recebida
        self.view_device_chat.addItem(f"Response: {command}")

    def execute_prog(self):
        send = (
            not self.ck_send_request.isChecked()
        )  # Verifica se é um envio de solicitação ou mensagem
        address = (
            str(self.le_address.text()).strip().upper()
        )  # Obtém o endereço da interface
        func = self.cb_functions.currentText()[0].upper()  # Obtém a função selecionada

        # Ajusta a função se for "get message"
        if str(self.cb_functions.currentText()) == "get message":
            func = "M"

        # Obtém os dados do campo de texto e ajusta o tamanho máximo
        data = self.te_translate_text.toPlainText()[:51].lower()
        if len(data) == 0:
            data = " "  # Define um espaço em branco se não houver dados
        len_data = str(len(data)).zfill(
            2
        )  # Calcula o tamanho dos dados e preenche com zeros à esquerda

        # Cria a mensagem com endereço, função, comprimento dos dados e os dados
        message = address + func + len_data + data
        print(f"Frame created: {message}")

        # Calcula o CRC16 usando o protocolo xmodem
        crc16_val = crc16_xmodem.new(message.encode()).crcValue
        message += str(crc16_val) + "\n"  # Adiciona o valor do CRC16 à mensagem

        # Envia o quadro de dados pela porta serial
        self.my_serial.send_frame(frame=message.encode())
        self.te_translate_text.clear()  # Limpa o campo de texto de entrada

        # Recebe a resposta do dispositivo
        response = self.my_serial.response_frame()
        if not response:
            response = ["ERROR"]  # Define "ERROR" se não houver resposta

        # Exibe as informações do CRC calculado, quadro enviado e resposta
        print(f"crc calculated: {crc16_val} : {hex(crc16_val)}")
        print(f"Frame sent: {message}")
        print(f"Response: ")
        [print(data) for data in response]  # Exibe todas as linhas da resposta

        # Atualiza o chat do PC e do dispositivo com os dados da mensagem e resposta
        self.view_pc_chat.addItem(
            f"PC: [addres, func, len_data, data, crc] = {address},{func},{len_data},{data},{str(crc16_val)}"
        )
        self.view_device_chat.addItem(f"Device: {response[0]}")

        # Verifica se o endereço foi preenchido
        if address != "":
            pass
        else:
            print(
                "Address not configured"
            )  # Mensagem de erro se o endereço não foi configurado

    def clear_chat(self):
        # Limpa os chats do PC e do dispositivo
        self.view_device_chat.clear()
        self.view_pc_chat.clear()

    def update_ck_send_request(self, _):
        # Limpa as funções da combobox
        self.cb_functions.clear()

        # Se o checkbox está marcado, configura para enviar solicitações
        if self.ck_send_request.isChecked():
            self.cb_functions.addItems(
                self._request_functions
            )  # Adiciona funções de solicitação
            self.ck_send_request.setText(
                "Request"
            )  # Altera o texto do checkbox para "Request"
            self.ck_send_request.setStyleSheet(
                "QCheckBox { font-style: italic;}"
            )  # Altera o estilo do checkbox
            self.te_translate_text.hide()  # Esconde o campo de entrada de texto
            self.top_layout.addItem(self.horizontal_spacer)  # Adiciona espaçamento
        else:
            # Caso contrário, configura para envio de mensagens
            self.cb_functions.addItems(
                self._send_functions
            )  # Adiciona funções de envio
            self.ck_send_request.setText(
                "Send"
            )  # Altera o texto do checkbox para "Send"
            self.ck_send_request.setStyleSheet(
                "QCheckBox { font-style: normal;}"
            )  # Restaura o estilo normal
            self.top_layout.removeItem(self.horizontal_spacer)  # Remove o espaçamento
            self.te_translate_text.setSizePolicy(
                QSizePolicy.Expanding, QSizePolicy.Preferred
            )  # Redefine o tamanho do campo de texto
            self.te_translate_text.show()  # Mostra o campo de entrada de texto


# Classe que gerencia a comunicação serial
class MySerial:
    def __init__(self, port="COM1", baudrate=9600, parity="N", stopbits=1) -> None:
        self.port = port  # Porta COM
        self.baudrate = baudrate  # Baudrate
        self.parity = parity  # Paridade
        self.stopbits = stopbits  # Bits de parada
        # Inicializa a instância da conexão serial
        self.serial = Serial(
            port=port, baudrate=baudrate, parity=parity, stopbits=stopbits
        )

    # Método para enviar um quadro de dados pela serial
    def send_frame(self, frame):
        self.serial.write(frame)  # Envia os dados pela porta serial

    # Método para receber uma resposta do dispositivo via serial
    def response_frame(self):
        self.serial.timeout = 1  # Define um tempo limite para a resposta
        response = self.serial.read_until(
            b"\n"
        )  # Lê a resposta até encontrar uma nova linha

        # Continua lendo enquanto houver dados disponíveis na porta serial
        while self.serial.in_waiting > 0:
            response += self.serial.read_until(b"\n")
        return response.decode(
            "utf-8"
        ).splitlines()  # Decodifica e divide as linhas da resposta


if __name__ == "__main__":
    app = QApplication([])
    win = ArduinoGUISerial()
    win.show()
    app.exec()
