import smbus
import subprocess

class OnoI2CDevice(object):
	_i2c = smbus.SMBus(1)

	def __init__(self, addr):
		self._addr = addr

	def _write8(self, reg, data):
		return self._i2c.write_byte_data(self._addr, reg, data)

	def _read8(self, reg):
		return self._i2c.read_byte_data(self._addr, reg)

	def _write16(self, reg, data):
		value = value & 0xFFFF
		self._i2c.write_word_data(self._addr, reg, data)

	def _read16(self, reg):
		return self._i2c.read_word_data(self._addr, reg) & 0xFFFF

	def _require_repeated_start(self):
		subprocess.check_call('chmod 666 /sys/module/i2c_bcm2708/parameters/combined', shell=True)
		subprocess.check_call('echo -n 1 > /sys/module/i2c_bcm2708/parameters/combined', shell=True)
