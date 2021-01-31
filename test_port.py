import serial


class ComPort:
    speeds = [2400, 4800, 9600, 19200, 38400, 57600, 115200]

    def __init__(self, port='COM5', speed=9600, timeout=200):
        self.com_port = serial.Serial()
        self.com_port.baudrate = speed
        self.com_port.port = port
        self.com_port.timeout = timeout
        self.com_port.open()
        print('Connected')

    @staticmethod
    def available_ports():
        ports = [f'COM{i}' for i in range(16)]
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def get_content(self):
        # self.com_port.open()
        data = []

        while not data:
            data = self.com_port.readline()
            data = data.strip().decode('UTF-8')[:-1].split(';')
            self.com_port.flushInput()
        print(data)
        return data

    def close(self):
        self.com_port.close()
        print('Disconnected')


if __name__ == '__main__':
    # print(ComPort.available_ports())
    opened = ComPort()
    print(opened.get_content())
    opened.close()

