import time
import spidev
import threading

# SPI COMMANDS
# > GENERAL                  IN  OUT
CMD_NOP             =  0   # 0   0    No operation
CMD_NC              =  255 # 0   0    Not connected
CMD_PING            =  1   # 0   1    To check connection
CMD_READ            =  2   # 0   ?    Return result from previous command
CMD_RESET           =  3   # 0   0    Reset the ATmega328
CMD_LEDON           =  4   # 0   0    Turn LED on
CMD_LEDOFF          =  5   # 0   0    Turn LED off

# > I2C                      IN  OUT
CMD_I2C_DETECT      =  20  # 1   1    Test if there's a device at addr
CMD_I2C_READ8       =  21  # 2   1    Read byte
CMD_I2C_WRITE8      =  22  # 3   0    Write byte
CMD_I2C_READ16      =  23  # 2   2    Read 2 bytes
CMD_I2C_WRITE16     =  24  # 4   0    Write 2 bytes

# > SERVO                    IN  OUT
CMD_SERVO_INIT      =  40  # 0   0    Init PCA9685
CMD_SERVO_ENABLE    =  41  # 0   0    Turn on MOSFET
CMD_SERVO_DISABLE   =  42  # 0   0    Turn off MOSFET
CMD_SERVO_NEUTRAL   =  43  # 0   0    Set all servos to 1500
CMD_SERVO_SET       =  44  # 3   0    Set 1 servo position
CMD_SERVO_SETALL    =  45  # 32  0    Set  position of all servos

# > CAPACITIVE TOUCH         IN  OUT
CMD_CAP_INIT        =  60  # 3   0    Init MPR121
CMD_CAP_SETTH       =  61  # 3   0    Set pin touch/release threshold
CMD_CAP_GETFD       =  62  # 0   24   Get pin filtered data (10 bits per electrode)
CMD_CAP_GETBD       =  63  # 1   1    Get pin baseline data, high 8 bits of 10
CMD_CAP_TOUCHED     =  64  # 0   2    Get touched status
CMD_CAP_SETGPIO     =  65  # 2   0    Set GPIO mode
CMD_CAP_GPIOREAD    =  66  # 0   1    Read GPIO pin
CMD_CAP_GPIOWRITE   =  67  # 2   0    Write GPIO pin

# > NEOPIXEL                 IN  OUT
CMD_NEO_INIT        =  80  # 1   0    Init Neopixel
CMD_NEO_ENABLE      =  81  # 0   0    Turn on MOSFET
CMD_NEO_DISABLE     =  82  # 0   0    Turn off MOSFET
CMD_NEO_SETBRIGHT   =  83  # 1   0    Set brightness
CMD_NEO_SHOW        =  84  # 0   0    Show pixels
CMD_NEO_SET         =  85  # 4   0    Set single pixel
CMD_NEO_SETRANGE    =  86  # 5   0    Set range of pixels
CMD_NEO_SETALL      =  87  # 3   0    Set all pixels
CMD_NEO_SETHSV      =  88  # 4   0    Set single pixel HSV
CMD_NEO_SETRANGEHSV =  89  # 5   0    Set range of pixels HSV
CMD_NEO_SETALLHSV   =  90  # 3   0    Set all pixels HSV

# > ANALOG                   IN  OUT
CMD_ANA_GET         = 100  # 1   2    Read an analog channel
CMD_ANA_GETALL      = 101  # 0   8    Read all analog channels

# MPR121 GPIO constants
GPIO_INPUT          = 1
GPIO_INPUT_PU       = 2
GPIO_INPUT_PD       = 3
GPIO_OUTPUT         = 4
GPIO_OUTPUT_HS      = 5
GPIO_OUTPUT_LS      = 6
GPIO_HIGH           = True
GPIO_LOW            = False

class _Hardware(object):
	def __init__(self):
		# Add a global lock that can be used to coordinate concurrent access to
		# the hardware class from multiple threads.
		self.lock = threading.Lock()

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
		self.spi.max_speed_hz = 122000 # 122kHz

	def __del__(self):
		pass

	def spi_command(self, cmd, params=None, returned=0, delay=0):
		"""
		Send a command over the SPI bus to the ATmega328.
		Optionally reads the result buffer and returns those bytes.
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

	# > GENERAL
	def ping(self):
		"""Returns True if OpSoRoHAT rev3 is connected."""
		return self.spi_command(CMD_PING, returned=1)[0] == 0xAA

	def reset(self):
		"""Resets the ATmega328, MPR121 and PCA9685."""
		self.spi_command(CMD_RESET, delay=2)

	def led_on(self):
		"""Turns status LED on."""
		self.spi_command(CMD_LEDON)

	def led_off(self):
		"""Turns status LED off."""
		self.spi_command(CMD_LEDOFF)

	# > I2C
	def i2c_detect(self, addr):
		"""Returns True if an I2C device is found at a particular address."""
		return self.spi_command(CMD_I2C_DETECT, params=[addr], returned=1)[0] == 1

	def i2c_read8(self, addr, reg):
		"""Read a byte from an I2C device."""
		return self.spi_command(CMD_I2C_READ8, params=[addr, reg], returned=1)[0]

	def i2c_write8(self, addr, reg, data):
		"""Write a byte to an I2C device."""
		self.spi_command(CMD_I2C_WRITE8, params=[addr, reg, data])

	def i2c_read16(self, addr, reg):
		"""Read 2 bytes from an I2C device."""
		data = self.spi_command(CMD_I2C_READ16, params=[addr, reg], returned=2)
		return (data[0] << 8) | data[1]

	def i2C_write16(self, addr, reg, data):
		"""Write 2 bytes to an I2C device."""
		val1 = (data & 0xFF00) >> 8
		val2 = (data & 0x00FF)

		self.spi_command(CMD_I2C_WRITE16, params=[addr, reg, val1, val2])

	# > SERVO
	def servo_init(self):
		"""Set up the PCA9685 for driving servos."""
		self.spi_command(CMD_SERVO_INIT, delay=0.02)

	def servo_enable(self):
		"""Turns on the servo power MOSFET, enabling all servos."""
		self.spi_command(CMD_SERVO_ENABLE)

	def servo_disable(self):
		"""Turns off the servo power MOSFET, disabling all servos."""
		self.spi_command(CMD_SERVO_DISABLE)

	def servo_neutral(self):
		"""Set all servos to 1500us."""
		self.spi_command(CMD_SERVO_NEUTRAL)

	def servo_set(self, channel, pos):
		"""
		Set the position of one servo.
		Pos in us, 500 to 2500
		"""
		offtime = (pos+2)//4
		self.spi_command(CMD_SERVO_SET, params=[channel, offtime >> 8, offtime & 0x00FF])

	def servo_set_all(self, pos_list):
		"""Set position of all 16 servos using a list."""
		spi_params = []
		for pos in pos_list:
			if pos is None:
				# Tell FW not to update this servo
				spi_params.append(0xFF)
				spi_params.append(0xFF)
			else:
				offtime = (pos+2)//4
				spi_params.append(offtime >> 8)
				spi_params.append(offtime & 0x0FF)

		self.spi_command(CMD_SERVO_SETALL, params=spi_params, delay=0.008)

	# > CAPACITIVE TOUCH
	def cap_init(self, electrodes, gpios=0, autoconfig=True):
		"""Initialize the MPR121 capacitive touch sensor."""
		ac = 1 if autoconfig else 0
		self.spi_command(CMD_CAP_INIT, params=[electrodes, gpios, ac], delay=0.05)

	def cap_set_threshold(self, electrode, touch, release):
		"""Set an electrode's touch and release threshold."""
		self.spi_command(CMD_CAP_SETTH, params=[electrode, touch, release])

	def cap_get_filtered_data(self):
		"""Get list of electrode filtered data (10 bits per electrode)."""
		data = []
		ret = Hardware.spi_command(CMD_CAP_GETFD, returned=24)
		for i in range(12):
			data.append(ret[i*2] + (ret[i*2+1] << 8))
		return data

	def cap_get_baseline_data(self):
		"""
		Get list of electrode baseline data.
		Result is 10 bits, but the 2 least significant bits are set to 0.
		"""
		data = Hardware.spi_command(CMD_CAP_GETBD, returned=12)
		# High 8 bits of 10 are returned.
		# Shift 2 so it's the same order of magnitude as cap_get_filtered_data().
		data = map(lambda x: x << 2, data)
		return data

	def cap_get_touched(self):
		"""
		Returns the values of the touch registers,
		each bit corresponds to one electrode.
		"""
		data = self.spi_command(CMD_CAP_TOUCHED, returned=2)
		return (data[0] << 8) | data[1]

	def cap_set_gpio_pinmode(self, gpio, pinmode):
		"""Sets a GPIO channel's pin mode."""
		bitmask = 1 << gpio
		self.spi_command(CMD_CAP_SETGPIO, params=[bitmask, pinmode])

	def cap_read_gpio(self):
		"""
		Returns the status of all GPIO channels,
		each bit corresponds to one gpio channel
		"""
		# TODO: Add optional pin parameter
		return self.spi_command(CMD_CAP_GPIOREAD)

	def cap_write_gpio(self, gpio, data):
		"""Set GPIO channel value."""
		bitmask = 1 << gpio
		setclr = 1 if data else 0
		self.spi_command(CMD_CAP_GPIOWRITE, params=[bitmask, setclr])

	# > NEOPIXEL
	def neo_init(self, num_leds):
		"""Initialize the NeoPixel library."""
		self.spi_command(CMD_NEO_INIT, params=[num_leds])

	def neo_enable(self):
		"""
		Turns on the NeoPixel MOSFET, enabling the NeoPixels.
		Data is lost when pixels are disabled, so call neo_show() again afterwards.
		"""
		self.spi_command(CMD_NEO_ENABLE)

	def neo_disable(self):
		"""
		Turns off the NeoPixel MOSFET, disabling the NeoPixels.
		Data is lost when pixels are disabled.
		"""
		self.spi_command(CMD_NEO_DISABLE)

	def neo_set_brightness(self, brightness):
		"""Set the NeoPixel's global brightness, 0-255."""
		self.spi_command(CMD_NEO_SETBRIGHT, params=[brightness])

	def neo_show(self):
		"""Sends the pixel data from the ATmega328 to the NeoPixels."""
		self.spi_command(CMD_NEO_SHOW)

	def neo_set_pixel(self, pixel, r, g, b):
		"""Set the color of a single pixel."""
		self.spi_command(CMD_NEO_SET, params=[pixel, r, g, b])

	def neo_set_range(self, start, end, r, g, b):
		"""Set the color of a range of pixels."""
		self.spi_command(CMD_NEO_SETRANGE, params=[start, end, r, g, b])

	def neo_set_all(self, r, g, b):
		"""Set the color of the entire strip."""
		self.spi_command(CMD_NEO_SETALL, params=[r, g, b])

	def neo_set_pixel_hsv(self, pixel, h, s, v):
		"""Set the HSV color of a single pixel."""
		self.spi_command(CMD_NEO_SETHSV, params=[pixel, h, s, v])

	def neo_set_range_hsv(self, start, end, h, s, v):
		"""Set the HSV color of a range of pixels."""
		self.spi_command(CMD_NEO_SETRANGEHSV, params=[start, end, h, s, v])

	def neo_set_all_hsv(self, h, s, v):
		"""Set the HSV color of the entire strip."""
		self.spi_command(CMD_NEO_SETALLHSV, params=[h, s, v])

	# > ANALOG
	def ana_read_channel(self, channel):
		"""Reads the value of a single analog channel."""
		data = self.spi_command(CMD_ANA_GET, params=[channel], returned=2)
		return data[0] << 8 | data[1]

	def ana_read_all_channels(self):
		"""Reads all analog channels and returns them as a list"""
		data = self.spi_command(CMD_ANA_GETALL, returned=2)
		return [
			data[0] << 8 | data[1],
			data[2] << 8 | data[3],
			data[4] << 8 | data[5],
			data[6] << 8 | data[7]
		]

	# Methods for backward compatibility
	servo_power_on = servo_enable
	servo_power_off = servo_disable
	set_servo_us = servo_set

	def set_all_servo_us(self, us):
		if us == 1500:
			self.servo_neutral()
		else:
			pos_list = [us for i in range(16)]
			self.servo_set_all(pos_list)

# Global instance that can be accessed by apps and scripts
Hardware = _Hardware()
Hardware.spi_command(CMD_RESET)
