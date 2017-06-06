from opsoro.console_msg import print_spi

class SpiDev(object):
    def __init__(self):
        self.mode = None
        self.max_speed_hz = 0
        print_spi('No SPI installed, using dummy class')

    def open(self,*args):
        # print_spi('open: {}'.format(args))
        pass

    def xfer2(self,*args):
        # print_spi('transfer: {}'.format(args))
        pass
