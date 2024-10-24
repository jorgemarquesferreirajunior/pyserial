import serial
from serial.tools import list_ports

ports = list_ports.comports()

available_ports = [port.description for port in ports]

[print(port) for port in available_ports if "n/a" not in port]
