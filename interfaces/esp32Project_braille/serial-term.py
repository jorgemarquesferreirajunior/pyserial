import serial 
from serial.tools import list_ports

ports = list_ports.comports()

av_ports = [port.device for port in ports if "n/a" not in port.description]

if av_ports:
    [print(f"{i+1}: {v}") for i, v in enumerate(av_ports)]
    ch = int(input("Escolha uma porta: "))
    my_port = av_ports[ch-1]

    my_serial = serial.Serial(port=my_port, baudrate=9600)
    if my_serial.is_open:
        while True:
            msg = str(input("Command: ")).strip().lower()
            if msg == "exit":
                my_serial.close()
                break
            else:
                msg += "\n"
                my_serial.write(msg.encode())
else:
    print("Nothing portCOM found! Check the USB connection")

