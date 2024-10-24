import serial
from serial.tools import list_ports

ports = list_ports.comports()

av_ports = [port.description for port in ports if "n/a" not in port]

print(av_ports[0])
myserial = serial.Serial(baudrate=9600, port=f"/dev/{av_ports[0]}")
print(myserial.is_open)

while True:
    cmd = str(input("Enviar comando? ")).strip().lower()
    if cmd == "exit":
        break
    data = str(input("Comando: "))

    myserial.write(data.encode())

myserial.close()
