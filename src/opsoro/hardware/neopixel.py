from opsoro.hardware.spi import SPI


# > NEOPIXEL                IN  OUT
CMD_NEO_INIT        = 80  # 1   0    Init Neopixel
CMD_NEO_ENABLE      = 81  # 0   0    Turn on MOSFET
CMD_NEO_DISABLE     = 82  # 0   0    Turn off MOSFET
CMD_NEO_SETBRIGHT   = 83  # 1   0    Set brightness
CMD_NEO_SHOW        = 84  # 0   0    Show pixels
CMD_NEO_SET         = 85  # 4   0    Set single pixel
CMD_NEO_SETRANGE    = 86  # 5   0    Set range of pixels
CMD_NEO_SETALL      = 87  # 3   0    Set all pixels
CMD_NEO_SETHSV      = 88  # 4   0    Set single pixel HSV
CMD_NEO_SETRANGEHSV = 89  # 5   0    Set range of pixels HSV
CMD_NEO_SETALLHSV   = 90  # 3   0    Set all pixels HSV


class Neopixel(object):
    # > NEOPIXEL
    def init(self, num_leds):
        """
        Initialize the NeoPixel library.

        :param int num_leds:    number of neopixel leds.
        """
        SPI.command(CMD_NEO_INIT, params=[num_leds])

    def enable(self):
        """
    	Turns on the NeoPixel MOSFET, enabling the NeoPixels.
    	Data is lost when pixels are disabled, so call show() again afterwards.
    	"""
        SPI.command(CMD_NEO_ENABLE)

    def disable(self):
        """
    	Turns off the NeoPixel MOSFET, disabling the NeoPixels.
    	Data is lost when pixels are disabled.
    	"""
        SPI.command(CMD_NEO_DISABLE)

    def set_brightness(self, brightness):
        """
        Set the NeoPixel's global brightness, 0-255.

        :param int brightness:    brightness to set (0-255)
        """
        SPI.command(CMD_NEO_SETBRIGHT, params=[brightness])

    def show(self):
        """Sends the pixel data from the ATmega328 to the NeoPixels."""
        SPI.command(CMD_NEO_SHOW)

    def set_pixel(self, pixel, r, g, b):
        """
        Set the color of a single pixel.

        :param int pixel:   pixel index
        :param int r:       red color value (0-255)
        :param int g:       green color value (0-255)
        :param int b:       blue color value (0-255)
        """
        SPI.command(CMD_NEO_SET, params=[pixel, r, g, b])

    def set_range(self, start, end, r, g, b):
        """
        Set the color of a range of pixels.

        :param int start:   start index of led range
        :param int end:     end index of led range
        :param int r:       red color value (0-255)
        :param int g:       green color value (0-255)
        :param int b:       blue color value (0-255)
        """
        SPI.command(CMD_NEO_SETRANGE, params=[start, end, r, g, b])

    def set_all(self, r, g, b):
        """
        Set the color of the entire strip.

        :param int r:       red color value (0-255)
        :param int g:       green color value (0-255)
        :param int b:       blue color value (0-255)
        """
        SPI.command(CMD_NEO_SETALL, params=[r, g, b])

    def set_pixel_hsv(self, pixel, h, s, v):
        """
        Set the HSV color of a single pixel.

        :param int pixel:   pixel index
        :param int h:       hue color value (0-255)
        :param int s:       saturation color value (0-255)
        :param int v:       value color value (0-255)
        """
        SPI.command(CMD_NEO_SETHSV, params=[pixel, h, s, v])

    def set_range_hsv(self, start, end, h, s, v):
        """
        Set the HSV color of a range of pixels.

        :param int start:   start index of led range
        :param int end:     end index of led range
        :param int h:       hue color value (0-255)
        :param int s:       saturation color value (0-255)
        :param int v:       value color value (0-255)
        """
        SPI.command(CMD_NEO_SETRANGEHSV, params=[start, end, h, s, v])

    def set_all_hsv(self, h, s, v):
        """
        Set the HSV color of the entire strip.

        :param int h:       hue color value (0-255)
        :param int s:       saturation color value (0-255)
        :param int v:       value color value (0-255)
        """
        SPI.command(CMD_NEO_SETALLHSV, params=[h, s, v])
