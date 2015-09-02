# OLD OLD OLD
# TODO: remove and replace completely by hardware2

from onoi2cdevice import OnoI2CDevice

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

class TPA2016(OnoI2CDevice):
	def __init__(self, addr=0x58):
		super(TPA2016, self).__init__(addr=addr)

	def enable_channel(self, r, l):
		setup = self._read8(TPA2016_SETUP)

		if r:
			setup |= TPA2016_SETUP_R_EN
		else:
			setup &= ~TPA2016_SETUP_R_EN
		if l:
			setup |= TPA2016_SETUP_L_EN
		else:
			setup &= ~TPA2016_SETUP_L_EN

		self._write8(TPA2016_SETUP, setup)


	def set_gain(self, gain):
		g = gain
		if g > 30:
				g = 30
		elif g < -28:
				g = -28

		self._write8(TPA2016_GAIN, g)
		pass

	def get_gain(self):
		return self._read8(TPA2016_GAIN)

	def set_release_control(self, release):
		# only 6 bits!
		if release > 0x3F:
				return

		self._write8(TPA2016_REL, release)

	def set_attack_control(self, attack):
		# only 6 bits!
		if attack > 0x3F:
				return

		self._write8(TPA2016_ATK, attack)

	def set_hold_control(self, hold):
		# only 6 bits!
		if hold > 0x3F:
				return

		self._write8(TPA2016_HOLD, hold)

	def set_limit_level_on(self):
		agc = self._read8(TPA2016_AGCLIMIT)
		agc &= ~(0x80)
		self._write8(TPA2016_AGCLIMIT, agc)

	def set_limit_level_off(self):
		agc = self._read8(TPA2016_AGCLIMIT)
		agc |= 0x80
		self._write8(TPA2016_AGCLIMIT, agc)

	def set_limit_level(self, limit):
		if limit > 31:
				return

		agc = self._read8(TPA2016_AGCLIMIT)
		agc &= ~(0x1F)
		agc |= limit
		self._write8(TPA2016_AGCLIMIT, agc)

	def set_agc_compression(self, x):
		if x > 3:
				return # only 2 bits!

		agc = self._read8(TPA2016_AGC)
		agc &= ~(0x03)
		agc |= x # set the compression ratio.
		self._write8(TPA2016_AGC, agc)

	def set_agc_max_gain(self, x):
		if x > 12:
				return # max gain max is 12 (30dB)

		agc = self._read8(TPA2016_AGC)
		agc &= ~(0xF0) # mask off top 4 bits
		agc |= (x << 4) # set the max gain
		self._write8(TPA2016_AGC, agc)
