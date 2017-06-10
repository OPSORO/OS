import time
import threading

# > GENERAL                  IN  OUT
CMD_NOP = 0  # 0   0    No operation
CMD_NC = 255  # 0   0    Not connected
CMD_PING = 1  # 0   1    To check connection
CMD_RESET = 3  # 0   0    Reset the ATmega328
CMD_LEDON = 4  # 0   0    Turn LED on
CMD_LEDOFF = 5  # 0   0    Turn LED off


from spi import SPI
from usb_serial import Serial

from . import analog
from . import capacitive
from . import i2c
from . import neopixel
from . import servo

class _Hardware(object):
    def __init__(self):
        """
        Hardware class, used to communicate with the shield.
        """
        # Add a global lock that can be used to coordinate concurrent access to
        # the hardware class from multiple threads.
        self.lock = threading.Lock()

        # self.analog =
        self.Analog     = analog.Analog()
        self.Capacitive = capacitive.Capacitive()
        self.I2C        = i2c.I2C()
        self.Neopixel   = neopixel.Neopixel()
        self.Servo      = servo.Servo()
        self.SPI        = SPI
        self.Serial     = Serial

    def __del__(self):
        pass

    # > GENERAL
    def ping(self):
        """
        Returns True if OPSOROHAT rev3 is connected.

        :return:         True if shield is connected
        :rtype:          bool
        """
        return SPI.command(CMD_PING, returned=1)[0] == 0xAA

    def reset(self):
        """Resets the ATmega328, MPR121 and PCA9685."""
        SPI.command(CMD_RESET, delay=2)

    def led_on(self):
        """Turns status LED on."""
        SPI.command(CMD_LEDON)

    def led_off(self):
        """Turns status LED off."""
        SPI.command(CMD_LEDOFF)

# Global instance that can be accessed by apps and scripts
Hardware = _Hardware()
