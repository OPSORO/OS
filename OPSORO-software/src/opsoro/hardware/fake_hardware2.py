
import threading
from opsoro.hardware import _Hardware



class Fake_Hardware(object):
    """
        debug-class print message on console and send commands to real hardware
    """
    def __init__(self):
        # Add a global lock that can be used to coordinate concurrent access to
        # the hardware class from multiple threads.
        self.lock = threading.Lock()
        self.real_hardware = _Hardware()


    def __del__(self):
        pass

    def spi_command(self, cmd, params=None, returned=0, delay=0):
        """
        Send a command over the SPI bus to the ATmega328.
        Optionally reads the result buffer and returns those bytes.
        """
        # Send command
        cprint("SPI:\t cmd: {}\t params: {}\t returned: {}\t delay: {}".format(cmd,params,returned,delay))
        return self.real_hardware.spi_command(cmd, params, returned, delay)

    # > GENERAL
    def ping(self):
        """Returns True if OPSOROHAT rev3 is connected."""
        cprint("ping for OpsoroHat")
        return self.real_hardware.ping()

    def reset(self):
        """Resets the ATmega328, MPR121 and PCA9685."""
        cprint("reset ATmega328, MPR121 and PCA9685")
        return self.real_hardware.reset()

    def led_on(self):
        """Turns status LED on."""
        cprint("Turns status LED on")
        return self.real_hardware.led_on()

    def led_off(self):
        """Turns status LED off."""
        cprint("Turns status LED off")
        return self.real_hardware.led_off()

    # > I2C
    def i2c_detect(self, addr):
        """Returns True if an I2C device is found at a particular address."""
        cprint("Search for I2C device on adress {}".format(addr))
        return self.real_hardware.i2c_detect(addr)

    def i2c_read8(self, addr, reg):
        """Read a byte from an I2C device."""
        cprint("Read byte (8bit) from I2C device at address {}".format(addr))
        return self.real_hardware.i2c_read8(addr,reg)

    def i2c_write8(self, addr, reg, data):
        """Write a byte to an I2C device."""
        cprint("Write byte (8bit) to I2C device at address {}".format(addr))
        return self.real_hardware.i2c_write8(addr, reg, data)

    def i2c_read16(self, addr, reg):
        """Read 2 bytes from an I2C device."""
        cprint("Read byte (16bit) from I2C device at address {}".format(addr))
        return self.real_hardware.i2c_read16(addr, reg)

    def i2C_write16(self, addr, reg, data):
        """Write 2 bytes to an I2C device."""
        cprint("Write byte (8bit) to I2C device at address {}".format(addr))
        return self.real_hardware.i2C_write16(addr, reg, data)

    # > SERVO
    def servo_init(self):
        """Set up the PCA9685 for driving servos."""
        cprint("Set up the PCA9685 for driving servos.")
        return self.real_hardware.servo_init()

    def servo_enable(self):
        """Turns on the servo power MOSFET, enabling all servos."""
        cprint("Turns on the servo power MOSFET, enabling all servos")
        return self.real_hardware.servo_enable()

    def servo_disable(self):
        """Turns off the servo power MOSFET, disabling all servos."""
        cprint("Turns off the servo power MOSFET, disabling all servos")
        return self.real_hardware.servo_disable()

    def servo_neutral(self):
        """Set all servos to 1500us."""
        cprint("Set all servos to 1500us")
        return self.real_hardware.servo_neutral()

    def servo_set(self, channel, pos):
        """
		Set the position of one servo.
		Pos in us, 500 to 2500
		"""
        cprint("Set servo\t Channel: {}\t position: {}".format(channel,pos))
        return self.real_hardware.servo_set(channel, pos)

    def servo_set_all(self, pos_list):
        """Set position of all 16 servos using a list."""
        cprint("Set position of all 16 servos using a list: {}".format(str(pos_list)))
        return self.real_hardware.servo_set_all(pos_list)

    # > CAPACITIVE TOUCH
    def cap_init(self, electrodes, gpios=0, autoconfig=True):
        """Initialize the MPR121 capacitive touch sensor."""
        cprint("under construction")
        return self.real_hardware.cap_init(electrodes, gpios, autoconfig)

    def cap_set_threshold(self, electrode, touch, release):
        """Set an electrode's touch and release threshold."""
        cprint("under construction")
        return self.real_hardware.cap_set_threshold(electrode, touch, release)

    def cap_get_filtered_data(self):
        """Get list of electrode filtered data (10 bits per electrode)."""
        cprint("under construction")
        return self.real_hardware.cap_get_filtered_data()

    def cap_get_baseline_data(self):
        """
		Get list of electrode baseline data.
		Result is 10 bits, but the 2 least significant bits are set to 0.
		"""
        cprint("under construction")
        return self.real_hardware.cap_get_baseline_data()

    def cap_get_touched(self):
        """
		Returns the values of the touch registers,
		each bit corresponds to one electrode.
		"""
        cprint("under construction")
        return self.real_hardware.cap_get_touched()

    def cap_set_gpio_pinmode(self, gpio, pinmode):
        """Sets a GPIO channel's pin mode."""
        cprint("under construction")
        return self.real_hardware.cap_set_gpio_pinmode()

    def cap_read_gpio(self):
        """
		Returns the status of all GPIO channels,
		each bit corresponds to one gpio channel
		"""
        cprint("under construction")
        return self.real_hardware.cap_read_gpio()

    def cap_write_gpio(self, gpio, data):
        """Set GPIO channel value."""
        cprint("under construction")
        return self.real_hardware.cap_write_gpio()

    # > NEOPIXEL
    def neo_init(self, num_leds):
        """Initialize the NeoPixel library."""
        cprint("Initialize the NeoPixel library. Number of leds: {}".format(num_leds))
        return self.real_hardware.neo_init(num_leds)

    def neo_enable(self):
        """
		Turns on the NeoPixel MOSFET, enabling the NeoPixels.
		Data is lost when pixels are disabled, so call neo_show() again afterwards.
		"""
        cprint("Enabling the NeoPixels.")
        return self.real_hardware.neo_enable()

    def neo_disable(self):
        """
		Turns off the NeoPixel MOSFET, disabling the NeoPixels.
		Data is lost when pixels are disabled.
		"""
        cprint("Disabling the NeoPixels")
        return self.real_hardware.neo_disable()

    def neo_set_brightness(self, brightness):
        """Set the NeoPixel's global brightness, 0-255."""
        cprint("Set the NeoPixel's global brightness, {}".format(brightness))
        return self.real_hardware.neo_set_brightness(brightness)

    def neo_show(self):
        """Sends the pixel data from the ATmega328 to the NeoPixels."""
        cprint("Sends the pixel data from the ATmega328 to the NeoPixels")
        return self.real_hardware.neo_show()

    def neo_set_pixel(self, pixel, r, g, b):
        """Set the color of a single pixel."""
        cprint("Set the color of a single pixel. pixel: {} color: ({},{},{})".format(pixel,r,g,b))
        return self.real_hardware.neo_set_pixel(pixel, r, g, b)

    def neo_set_range(self, start, end, r, g, b):
        """Set the color of a range of pixels."""
        cprint("Set the color of a range of pixels. start: {} end:{} color: ({},{},{})".format(start,end,r,g,b))
        return self.real_hardware.neo_set_range(start, end, r, g, b)

    def neo_set_all(self, r, g, b):
        """Set the color of the entire strip."""
        cprint("Set the color of the entire strip. color: ({},{},{})".format(r,g,b))
        return self.real_hardware.neo_set_all(r, g, b)

    def neo_set_pixel_hsv(self, pixel, h, s, v):
        """Set the HSV color of a single pixel."""
        cprint("Set the HSV color of a single pixel. pixel: {} color: ({},{},{})".format(pixel,r,g,b))
        return self.real_hardware.neo_set_pixel_hsv(pixel, h, s, v)

    def neo_set_range_hsv(self, start, end, h, s, v):
        """Set the HSV color of a range of pixels."""
        cprint("Set the HSV color of a range of pixels. start: {} end:{} color: ({},{},{})".format(start,end,r,g,b))
        return self.real_hardware.neo_set_range_hsv(start, end, h, s, v)

    def neo_set_all_hsv(self, h, s, v):
        """Set the HSV color of the entire strip."""
        cprint("Set the HSV color of the entire strip. color: ({},{},{})".format(r,g,b))
        return self.real_hardware.neo_set_all_hsv(h, s, v)

    # > ANALOG
    def ana_read_channel(self, channel):
        """Reads the value of a single analog channel."""
        cprint("Reads the value of a single analog channel")
        return self.real_hardware.ana_read_channel(channel)

    def ana_read_all_channels(self):
        """Reads all analog channels and returns them as a list"""
        cprint("Reads all analog channels and returns them as a list")
        data = self.spi_command(CMD_ANA_GETALL, returned=2)
        return self.real_hardware.ana_read_all_channels()

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

def cprint(txt):
    print "\033[1m[\033[94m HARDWARE \033[0m\033[1m]\033[0m %s" % txt
