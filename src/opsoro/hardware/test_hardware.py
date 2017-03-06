class Dummy_Hardware(object):
    def __init__(self):
        """
        Hardware class, used to communicate with the shield.
        """
        pass

    def __del__(self):
        pass

    def spi_command(self, cmd, params=None, returned=0, delay=0):
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
        return []

    # > GENERAL
    def ping(self):
        """
        Returns True if OPSOROHAT rev3 is connected.

        :return:         True if shield is connected
        :rtype:          bool
        """
        return True

    def reset(self):
        """Resets the ATmega328, MPR121 and PCA9685."""
        pass

    def led_on(self):
        """Turns status LED on."""
        pass

    def led_off(self):
        """Turns status LED off."""
        pass

    # > I2C
    def i2c_detect(self, addr):
        """
        Returns True if an I2C device is found at a particular address.

        :param int addr:   address of the I2C device.

        :return:         I2C device detected
        :rtype:          bool
        """
        return True

    def i2c_read8(self, addr, reg):
        """
        Read a Byte from an I2C device.

        :param int addr:    address of the I2C device.
        :param int reg:     register address in the I2C device

        :return:         what is the function returning?
        :rtype:          var
        """
        return 0

    def i2c_write8(self, addr, reg, data):
        """
        Write a Byte to an I2C device.

        :param int addr:    address of the I2C device.
        :param int reg:     register address in the I2C device
        :param var data:    Byte to send
        """
        pass

    def i2c_read16(self, addr, reg):
        """
        Read 2 bytes from an I2C device.

        :param int addr:    address of the I2C device.
        :param int reg:     register address in the I2C device

        :return:         2 Bytes
        :rtype:          var
        """

        return 0

    def i2C_write16(self, addr, reg, data):
        """
        Write 2 bytes to an I2C device.

        :param int addr:    address of the I2C device.
        :param int reg:     register address in the I2C device
        :param var data:    Bytes to send
        """
        pass

    # > SERVO
    def servo_init(self):
        """Set up the PCA9685 for driving servos."""
        pass

    def servo_enable(self):
        """Turns on the servo power MOSFET, enabling all servos."""
        pass

    def servo_disable(self):
        """Turns off the servo power MOSFET, disabling all servos."""
        pass

    def servo_neutral(self):
        """Set all servos to 1500us."""
        pass

    def servo_set(self, channel, pos):
        """
		Set the position of one servo.
		Pos in us, 500 to 2500

        :param int channel: channel of the servo
        :param int pos:     position of the servo (500 to 2500)
        """
        pass

    def servo_set_all(self, pos_list):
        """
        Set position of all 16 servos using a list.

        :param list pos_list:   list of servo positions
        """
        pass

    # > CAPACITIVE TOUCH
    def cap_init(self, electrodes, gpios=0, autoconfig=True):
        """
        Initialize the MPR121 capacitive touch sensor.

        :param int electrodes:  amount of electrodes
        :param int gpios:       amount of gpios
        :param bool autoconfig:
        """
        pass

    def cap_set_threshold(self, electrode, touch, release):
        """
        Set an electrode's touch and release threshold.

        :param int electrode:   index of electrode
        :param int touch:       threshold value for touch detection
        :param int release:     threshold value for release detection
        """
        pass

    def cap_get_filtered_data(self):
        """
        Get list of electrode filtered data (10 bits per electrode).

        :return:        electrode filtered data (10 bits per electrode).
        :rtype:         list
        """
        return []

    def cap_get_baseline_data(self):
        """
		Get list of electrode baseline data.
		Result is 10 bits, but the 2 least significant bits are set to 0.

        :return:        electrode baseline data (10 bits).
        :rtype:         list
		"""
        return []

    def cap_get_touched(self):
        """
		Returns the values of the touch registers,
		each bit corresponds to one electrode.

        :return:        values of the touch registers,
        :rtype:         list
		"""
        return []

    def cap_set_gpio_pinmode(self, gpio, pinmode):
        """
        Sets a GPIO channel's pin mode.

        :param int gpio:    gpio channel
        :param int pinmode: pinmode to set
        """
        pass

    def cap_read_gpio(self):
        """
		Returns the status of all GPIO channels,
		each bit corresponds to one gpio channel.

        :return:         status of all GPIO channels.
        :rtype:          list
		"""
        return []

    def cap_write_gpio(self, gpio, data):
        """
        Set GPIO channel value.

        :param int gpio:   gpio channel
        :param int data:   data to write to gpio channel.
        """
        pass

    # > NEOPIXEL
    def neo_init(self, num_leds):
        """
        Initialize the NeoPixel library.

        :param int num_leds:    number of neopixel leds.
        """
        pass

    def neo_enable(self):
        """
		Turns on the NeoPixel MOSFET, enabling the NeoPixels.
		Data is lost when pixels are disabled, so call neo_show() again afterwards.
		"""
        pass

    def neo_disable(self):
        """
		Turns off the NeoPixel MOSFET, disabling the NeoPixels.
		Data is lost when pixels are disabled.
		"""
        pass

    def neo_set_brightness(self, brightness):
        """
        Set the NeoPixel's global brightness, 0-255.

        :param int brightness:    brightness to set (0-255)
        """
        pass

    def neo_show(self):
        """Sends the pixel data from the ATmega328 to the NeoPixels."""
        pass

    def neo_set_pixel(self, pixel, r, g, b):
        """
        Set the color of a single pixel.

        :param int pixel:   pixel index
        :param int r:       red color value (0-255)
        :param int g:       green color value (0-255)
        :param int b:       blue color value (0-255)
        """
        pass

    def neo_set_range(self, start, end, r, g, b):
        """
        Set the color of a range of pixels.

        :param int start:   start index of led range
        :param int end:     end index of led range
        :param int r:       red color value (0-255)
        :param int g:       green color value (0-255)
        :param int b:       blue color value (0-255)
        """
        pass

    def neo_set_all(self, r, g, b):
        """
        Set the color of the entire strip.

        :param int r:       red color value (0-255)
        :param int g:       green color value (0-255)
        :param int b:       blue color value (0-255)
        """
        pass

    def neo_set_pixel_hsv(self, pixel, h, s, v):
        """
        Set the HSV color of a single pixel.

        :param int pixel:   pixel index
        :param int h:       hue color value (0-255)
        :param int s:       saturation color value (0-255)
        :param int v:       value color value (0-255)
        """
        pass

    def neo_set_range_hsv(self, start, end, h, s, v):
        """
        Set the HSV color of a range of pixels.

        :param int start:   start index of led range
        :param int end:     end index of led range
        :param int h:       hue color value (0-255)
        :param int s:       saturation color value (0-255)
        :param int v:       value color value (0-255)
        """
        pass

    def neo_set_all_hsv(self, h, s, v):
        """
        Set the HSV color of the entire strip.

        :param int h:       hue color value (0-255)
        :param int s:       saturation color value (0-255)
        :param int v:       value color value (0-255)
        """
        pass

    # > ANALOG
    def ana_read_channel(self, channel):
        """
        Reads the value of a single analog channel.

        :param int channel:     analog channel to read

        :return:         analog value of the channel
        :rtype:          var
        """
        return 0

    def ana_read_all_channels(self):
        """
        Reads all analog channels and returns them as a list.

        :return:         analog values
        :rtype:          list
        """
        return []

    # Methods for backward compatibility
    # servo_power_on = servo_enable
    # servo_power_off = servo_disable
    # set_servo_us = servo_set

    def set_all_servo_us(self, us):
        """
        Set all servos to a certain position (us)

        :param int us:   position in us
        """
        if us == 1500:
            self.servo_neutral()
        else:
            pos_list = [us for i in range(16)]
            self.servo_set_all(pos_list)

# Global instance that can be accessed by apps and scripts
Hardware = Dummy_Hardware()
