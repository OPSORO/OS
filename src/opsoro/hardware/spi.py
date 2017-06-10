# SPI COMMANDS

CMD_READ                = 2  # 0   ?    Return result from previous command
CMD_RESET               = 3  # 0   0    Reset the ATmega328

import time
try:
    import spidev
except ImportError:
    import dummy_spidev as spidev

class _SPI(object):
    def __init__(self):
        """
        SPI class, used to communicate with the shield.
        """
        # Setup SPI
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 0b00

        # TODO: Further testing of SPI speeds
        # NeoKeypad.lua started showing strange behavior at 500kHz.
        # Presumably because neo_show() disables interrupts momentarily,
        # Causing the ATmega328 to miss SPI interrupts
        # Touch app shows spikes at 250kHz, but not at 122kHz.

        #self.spi.max_speed_hz = 50000 # 50kHz
        #self.spi.max_speed_hz = 500000 # 500kHz
        #self.spi.max_speed_hz = 250000 # 250kHz
        self.spi.max_speed_hz = 122000  # 122kHz

    def command(self, cmd, params=None, returned=0, delay=0):
        """
		Send a command over the SPI bus to the ATmega328.
		Optionally reads the result buffer and returns those Bytes.

        :param string cmd:    spi command
        :param strin params:  parameters for the command
        :param int returned:  size of result reading
        :param int delay:     delay between sending the command and reading the result

        :return:         result buffer (Bytes)
        :rtype:          list
        """
        # Send command
        if params:
            self.spi.xfer2([cmd] + params)
        else:
            self.spi.xfer2([cmd])

        # Delay
        if delay:
            time.sleep(delay)

        # Read result
        if returned:
            data = self.spi.xfer2([CMD_READ] + [255 for i in range(returned)])
            # First byte is junk, this is due to the way SPI works
            return data[1:]
        else:
            return


SPI = _SPI()
SPI.command(CMD_RESET)
