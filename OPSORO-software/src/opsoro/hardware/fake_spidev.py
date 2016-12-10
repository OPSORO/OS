
class SpiDev(object):
    def __init__(self):
        self.mode = None
        self.max_speed_hz = 0

    def open(self,*args):
        cprint("open: {}".format(args))

    def xfer2(self,*args):
        cprint("transfer: {}".format(args))

def cprint(txt):
    print "\033[1m[\033[94m SPI \033[0m\033[1m]\033[0m %s" % txt

