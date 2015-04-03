from onoi2cdevice import OnoI2CDevice

MPR121_I2CADDR_DEFAULT = 0x5A
MPR121_TOUCHSTATUS_L   = 0x00
MPR121_TOUCHSTATUS_H   = 0x01
MPR121_FILTDATA_0L     = 0x04
MPR121_FILTDATA_0H     = 0x05
MPR121_BASELINE_0      = 0x1E
MPR121_MHDR            = 0x2B
MPR121_NHDR            = 0x2C
MPR121_NCLR            = 0x2D
MPR121_FDLR            = 0x2E
MPR121_MHDF            = 0x2F
MPR121_NHDF            = 0x30
MPR121_NCLF            = 0x31
MPR121_FDLF            = 0x32
MPR121_NHDT            = 0x33
MPR121_NCLT            = 0x34
MPR121_FDLT            = 0x35
MPR121_TOUCHTH_0       = 0x41
MPR121_RELEASETH_0     = 0x42
MPR121_DEBOUNCE        = 0x5B
MPR121_CONFIG1         = 0x5C
MPR121_CONFIG2         = 0x5D
MPR121_CHARGECURR_0    = 0x5F
MPR121_CHARGETIME_1    = 0x6C
MPR121_ECR             = 0x5E
MPR121_AUTOCONFIG0     = 0x7B
MPR121_AUTOCONFIG1     = 0x7C
MPR121_UPLIMIT         = 0x7D
MPR121_LOWLIMIT        = 0x7E
MPR121_TARGETLIMIT     = 0x7F

MPR121_GPIOCTL0        = 0x73
MPR121_GPIOCTL1        = 0x74
MPR121_GPIODATA        = 0x75
MPR121_GPIODIR         = 0x76
MPR121_GPIOEN          = 0x77
MPR121_GPIOSET         = 0x78
MPR121_GPIOCLR         = 0x79
MPR121_GPIOTOGGLE      = 0x7A

MPR121_SOFTRESET       = 0x80


GPIO_INPUT             = 1
GPIO_INPUT_PU          = 2
GPIO_INPUT_PD          = 3
GPIO_OUTPUT            = 4
GPIO_OUTPUT_HS         = 5
GPIO_OUTPUT_LS         = 6

class MPR121Ext(OnoI2CDevice):
	def __init__(self, addr=0x5A, electrodes=0, gpios=0, autoconfig=True):
		"""
		MPR121 capactive touch sensor.
		Functionality extended to include autoconfig and GPIO usage.
		Based on the Adafruit MPR121.py library and the Bare Conductive
		MPR121 library for arduino.

		Args:
			addr: I2C address of the MPR121 chip.
			electrodes: Number of electrodes, max 12.
			  Starts at ELE0, e.g. 5 means ELE0-ELE4 are enabled.
			gpios: Number of GPIO pins, starts at pin 11.
			  E.g.: a value of 4 means pin 11, 10, 9 and 8 are enabled as GPIOs
			  Maximum 8 pins can be used as GPIOs.
			  Not implemented.
			autoconfig: Let the MPR121 configure determine electrode
			  charge current and charge time automatically.
		"""
		# TODO: Implement GPIO

		assert electrodes + gpios <= 12, "More electrodes+GPIOs than there are available pins"

		super(MPR121Ext, self).__init__(addr=addr)

		self._electrodes = electrodes
		self._gpios = gpios

		self._require_repeated_start()

		# Reset and put in stop mode
		self._write8(MPR121_SOFTRESET, 0x63)
		self._write8(MPR121_ECR, 0x00)

		# Touch pad baseline filter
		# Rising
		self._write8(MPR121_MHDR, 0x01) # Max half delta rising
		self._write8(MPR121_NHDR, 0x01) # Noise half delta rising
		self._write8(MPR121_NCLR, 0x0E) # Noise count limit rising
		self._write8(MPR121_FDLR, 0x00) # Delay limit rising
		# Falling
		self._write8(MPR121_MHDF, 0x2F) # Max half delta falling
		self._write8(MPR121_NHDF, 0x30) # Noise half delta falling
		self._write8(MPR121_NCLF, 0x31) # Noise count limit falling
		self._write8(MPR121_FDLF, 0x32) # Delay limit falling
		# Touched
		self._write8(MPR121_NHDT, 0x00) # Noise half delta touched
		self._write8(MPR121_NCLT, 0x00) # Noise counts touched
		self._write8(MPR121_FDLT, 0x00) # Filter delay touched

		# Touch pad threshold
		for i in range(12):
			#self.set_threshold(i, touch=10, release=6) # Default touch/release values
			self.set_threshold(i, touch=40, release=20) # Default touch/release values

		# touch / release debounce
		self._write8(MPR121_DEBOUNCE, 0x00)

		# response time = SFI(10) X ESI(8ms) = 80ms
		self._write8(MPR121_DEBOUNCE, 0x13);

		# FFI=18
		self._write8(MPR121_CONFIG1, 0x80);

		#Auto configuration
		if autoconfig:
			self._write8(MPR121_AUTOCONFIG0,0x8F);
			# charge to 70% of Vdd , high sensitivity
			self._write8(MPR121_UPLIMIT, 0xE4);
			self._write8(MPR121_LOWLIMIT, 0x94);
			self._write8(MPR121_TARGETLIMIT, 0xCD);

		# Set up electrode calibration
		ecr = 0b11000000 # Calibration Lock = 11, ELEPROX = 00
		ecr |= self._electrodes  # Set ELE_ENABLE
		self._write8(MPR121_ECR, ecr)

	def set_threshold(self, pin, touch, release):
		"""Set electrode touch and release threshold

		Args:
			pin: Electrode to configure, 0-11
			touch: Touch threshold, 0-255, should be higher than release threshold
			release: Release threshold, 0-255
		"""
		self._write8(MPR121_TOUCHTH_0 + 2*pin, touch)
		self._write8(MPR121_RELEASETH_0 + 2*pin, release)

	def filtered_data(self, pin):
		"""Returns the filtered data for a single electrode

		Args:
			pin: Electrode to read, 0-11
		"""
		return self._read16(MPR121_FILTDATA_0L + pin*2)

	def baseline_data(self, pin):
		"""Returns the baseline data for a single electrode

		Args:
			pin: Electrode to read, 0-11
		"""
		bl = self._read8(MPR121_BASELINE_0 + pin)
		return bl << 2

	def touched(self):
		"""Return touch state of all pins as a 12-bit value where each bit
		represents a pin, with a value of 1 being touched and 0 not being touched.
		"""
		# The lower 12 bits contain electrode touch status,
		# the 4 high bits contain ELEPROX and REXT over-current status (OVCF).
		t = self._read16(MPR121_TOUCHSTATUS_L)
		return t & 0x0FFF

	def gpio_pinmode(self, pin, mode):
		assert pin > (11 - self._gpios), "Pin not enabled as GPIO in __init__"
		assert pin >= self._electrodes, "Pin is used as electrode"
		assert pin > 3, "Pins 0-3 cannot be used as GPIO"

		bitmask = 1 << (pin - 4)

		en = self._read8(MPR121_GPIOEN)
		dir_ = self._read8(MPR121_GPIODIR)
		ctl0 = self._read8(MPR121_GPIOCTL0)
		ctl1 = self._read8(MPR121_GPIOCTL1)

		if mode == GPIO_INPUT:
			self._write8(MPR121_GPIOEN,   en   |  bitmask) # EN   = 1
			self._write8(MPR121_GPIODIR,  dir_ & ~bitmask) # DIR  = 0
			self._write8(MPR121_GPIOCTL0, ctl0 & ~bitmask) # CTL0 = 0
			self._write8(MPR121_GPIOCTL1, ctl1 & ~bitmask) # CTL1 = 0
		elif mode == GPIO_INPUT_PU:
			self._write8(MPR121_GPIOEN,   en   |  bitmask) # EN   = 1
			self._write8(MPR121_GPIODIR,  dir_ & ~bitmask) # DIR  = 0
			self._write8(MPR121_GPIOCTL0, ctl0 |  bitmask) # CTL0 = 1
			self._write8(MPR121_GPIOCTL1, ctl1 |  bitmask) # CTL1 = 1
		elif mode == GPIO_INPUT_PD:
			self._write8(MPR121_GPIOEN,   en   |  bitmask) # EN   = 1
			self._write8(MPR121_GPIODIR,  dir_ & ~bitmask) # DIR  = 0
			self._write8(MPR121_GPIOCTL0, ctl0 |  bitmask) # CTL0 = 1
			self._write8(MPR121_GPIOCTL1, ctl1 & ~bitmask) # CTL1 = 0
		elif mode == GPIO_OUTPUT:
			self._write8(MPR121_GPIOEN,   en   |  bitmask) # EN   = 1
			self._write8(MPR121_GPIODIR,  dir_ |  bitmask) # DIR  = 1
			self._write8(MPR121_GPIOCTL0, ctl0 & ~bitmask) # CTL0 = 0
			self._write8(MPR121_GPIOCTL1, ctl1 & ~bitmask) # CTL1 = 0
		elif mode == GPIO_OUTPUT_HS:
			self._write8(MPR121_GPIOEN,   en   |  bitmask) # EN   = 1
			self._write8(MPR121_GPIODIR,  dir_ |  bitmask) # DIR  = 1
			self._write8(MPR121_GPIOCTL0, ctl0 |  bitmask) # CTL0 = 1
			self._write8(MPR121_GPIOCTL1, ctl1 |  bitmask) # CTL1 = 1
		elif mode == GPIO_OUTPUT_LS:
			self._write8(MPR121_GPIOEN,   en   |  bitmask) # EN   = 1
			self._write8(MPR121_GPIODIR,  dir_ |  bitmask) # DIR  = 1
			self._write8(MPR121_GPIOCTL0, ctl0 |  bitmask) # CTL0 = 1
			self._write8(MPR121_GPIOCTL1, ctl1 & ~bitmask) # CTL1 = 0

	def gpio_read(self, pin):
		return (self._read8(MPR121_GPIODATA) >> (pin - 4) == 1)

	def gpio_write(self, pin, data):
		if data:
			self._write8(MPR121_GPIOSET, 1 << (pin - 4))
		else:
			self._write8(MPR121_GPIOCLR, 1 << (pin - 4))
