import smbus

TPA2016_SETUP           = 0x1
TPA2016_SETUP_R_EN      = 0x80
TPA2016_SETUP_L_EN      = 0x40
TPA2016_SETUP_SWS       = 0x20
TPA2016_SETUP_R_FAULT   = 0x10
TPA2016_SETUP_L_FAULT   = 0x08
TPA2016_SETUP_THERMAL   = 0x04
TPA2016_SETUP_NOISEGATE = 0x01

TPA2016_ATK             = 0x2
TPA2016_REL             = 0x3
TPA2016_HOLD            = 0x4
TPA2016_GAIN            = 0x5
TPA2016_AGCLIMIT        = 0x6
TPA2016_AGC             = 0x7
TPA2016_AGC_OFF         = 0x00
TPA2016_AGC_2           = 0x01
TPA2016_AGC_4           = 0x02
TPA2016_AGC_8           = 0x03

class TPA2016:
	i2c = smbus.SMBus(1)

	def __init__(self, addr=0x58):
		self.__addr = addr

	def __write(self, reg, data):
		return self.i2c.write_byte_data(self.__addr, reg, data)

	def __read(self, reg):
		return self.i2c.read_byte_data(self.__addr, reg)

	def enableChannel(self, r, l):
		setup = self.__read(TPA2016_SETUP)
		if r:
				setup |= TPA2016_SETUP_R_EN
		else:
				setup &= ~TPA2016_SETUP_R_EN
		if l:
				setup |= TPA2016_SETUP_L_EN
		else:
				setup &= ~TPA2016_SETUP_L_EN
		self.__write(TPA2016_SETUP, setup)


	def setGain(self, gain):
		g = gain
		if g > 30:
				g = 30
		elif g < -28:
				g = -28

		self.__write(TPA2016_GAIN, g)
		pass

	def getGain(self):
		return self.__read(TPA2016_GAIN)

	def setReleaseControl(self, release):
		# only 6 bits!
		if release > 0x3F:
				return

		self.__write(TPA2016_REL, release)

	def setAttackControl(self, attack):
		# only 6 bits!
		if attack > 0x3F:
				return

		self.__write(TPA2016_ATK, attack)

	def setHoldControl(self, hold):
		# only 6 bits!
		if hold > 0x3F:
				return

		self.__write(TPA2016_HOLD, hold)

	def setLimitLevelOn(self):
		agc = self.__read(TPA2016_AGCLIMIT)
		agc &= ~(0x80)
		self.__write(TPA2016_AGCLIMIT, agc)

	def setLimitLevelOff(self):
		agc = self.__read(TPA2016_AGCLIMIT)
		agc |= 0x80
		self.__write(TPA2016_AGCLIMIT, agc)

	def setLimitLevel(self, limit):
		if limit > 31:
				return

		agc = self.__read(TPA2016_AGCLIMIT)
		agc &= ~(0x1F);
		agc |= limit;
		self.__write(TPA2016_AGCLIMIT, agc)

	def setAGCCompression(self, x):
		if x > 3:
				return # only 2 bits!

		agc = self.__read(TPA2016_AGC);
		agc &= ~(0x03)
		agc |= x # set the compression ratio.
		self.__write(TPA2016_AGC, agc);

	def setAGCMaxGain(self, x):
		if x > 12:
				return # max gain max is 12 (30dB)

		agc = self.__read(TPA2016_AGC)
		agc &= ~(0xF0) # mask off top 4 bits
		agc |= (x << 4) # set the max gain
		self.__write(TPA2016_AGC, agc);
