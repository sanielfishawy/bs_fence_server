import serial
import io

class NextionIO:

    TERMINATOR = b'\xff\xff\xff'
    SER = serial.Serial('/dev/serial0', 9600)

    @classmethod
    def send_command(cls, command):
        cls.SER.write(str.encode(command) + cls.TERMINATOR)

    @classmethod
    def read_results(cls):
        res = ""
        term = 0
        while(True):
            char = cls.ser.read()
            if char == b'\xff':
                term += 1
            else:
                res += char
            if term >= 2:
                break
        return res





if __name__ == '__main__':
    # foo = NextionIO.send_command('t0.txt=\"bar\"')
    # foo = NextionIO.send_command('get t0.txt')
    pass
