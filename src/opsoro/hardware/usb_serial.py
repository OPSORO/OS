import serial as pyserial
import glob

from opsoro.console_msg import *

class _Serial(object):
    # > SERIAL
    def __init__(self):
        """Initialize serial."""
        self.ports = []
        self.port = None
        self.scan()

    def scan(self):
        visible_ports = glob.glob('/dev/ttyACM[0-9]*')
        self.ports = []
        for port in visible_ports:
            try:
                print_info(port)
                s = pyserial.Serial(port)
                s.close()
                self.ports.append(port)
            except Exception as e:
                print e
                pass
        print_info(self.ports)

    # def connect(self, port, baudrate):
    #     self.port = pyserial.Serial("/dev/ttyACM0", baudrate = 9600, timeout = 2)
    #     pass

    # def readline(self):
    #     pass

    def send(self, text, port_id=0, baudrate=9600):
        try:
            s = pyserial.Serial(self.ports[port_id], baudrate)
            s.write(text)
            s.close()
        except Exception as e:
            print_error('Error sending serial command.')

Serial = _Serial()
