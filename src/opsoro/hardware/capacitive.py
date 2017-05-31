from opsoro.hardware.spi import SPI

# > CAPACITIVE TOUCH         IN  OUT
CMD_CAP_INIT        = 60  # 3   0    Init MPR121
CMD_CAP_SETTH       = 61  # 3   0    Set pin touch/release threshold
CMD_CAP_GETFD       = 62  # 0   24   Get pin filtered data (10 bits per electrode)
CMD_CAP_GETBD       = 63  # 1   1    Get pin baseline data, high 8 bits of 10
CMD_CAP_TOUCHED     = 64  # 0   2    Get touched status
CMD_CAP_SETGPIO     = 65  # 2   0    Set GPIO mode
CMD_CAP_GPIOREAD    = 66  # 0   1    Read GPIO pin
CMD_CAP_GPIOWRITE   = 67  # 2   0    Write GPIO pin


# MPR121 GPIO constants
GPIO_INPUT      = 1
GPIO_INPUT_PU   = 2
GPIO_INPUT_PD   = 3
GPIO_OUTPUT     = 4
GPIO_OUTPUT_HS  = 5
GPIO_OUTPUT_LS  = 6
GPIO_HIGH       = True
GPIO_LOW        = False

class Capacitive(object):
    # > CAPACITIVE TOUCH
    def init(self, electrodes, gpios=0, autoconfig=True):
        """
        Initialize the MPR121 capacitive touch sensor.

        :param int electrodes:  amount of electrodes
        :param int gpios:       amount of gpios
        :param bool autoconfig:
        """
        ac = 1 if autoconfig else 0
        SPI.command(CMD_CAP_INIT, params=[electrodes, gpios, ac], delay=0.05)

    def set_threshold(self, electrode, touch, release):
        """
        Set an electrode's touch and release threshold.

        :param int electrode:   index of electrode
        :param int touch:       threshold value for touch detection
        :param int release:     threshold value for release detection
        """
        SPI.command(CMD_CAP_SETTH, params=[electrode, touch, release])

    def get_filtered_data(self):
        """
        Get list of electrode filtered data (10 bits per electrode).

        :return:        electrode filtered data (10 bits per electrode).
        :rtype:         list
        """
        data = []
        ret = SPI.command(CMD_CAP_GETFD, returned=24)
        for i in range(12):
            data.append(ret[i * 2] + (ret[i * 2 + 1] << 8))
        return data

    def get_baseline_data(self):
        """
    	Get list of electrode baseline data.
    	Result is 10 bits, but the 2 least significant bits are set to 0.

        :return:        electrode baseline data (10 bits).
        :rtype:         list
    	"""
        data = SPI.command(CMD_CAP_GETBD, returned=12)
        # High 8 bits of 10 are returned.
        # Shift 2 so it's the same order of magnitude as cap_get_filtered_data().
        data = map(lambda x: x << 2, data)
        return data

    def get_touched(self):
        """
    	Returns the values of the touch registers,
    	each bit corresponds to one electrode.

        :return:        values of the touch registers,
        :rtype:         list
    	"""
        data = SPI.command(CMD_CAP_TOUCHED, returned=2)
        return (data[0] << 8) | data[1]

    def set_gpio_pinmode(self, gpio, pinmode):
        """
        Sets a GPIO channel's pin mode.

        :param int gpio:    gpio channel
        :param int pinmode: pinmode to set
        """
        bitmask = 1 << gpio
        SPI.command(CMD_CAP_SETGPIO, params=[bitmask, pinmode])

    def read_gpio(self):
        """
    	Returns the status of all GPIO channels,
    	each bit corresponds to one gpio channel.

        :return:         status of all GPIO channels.
        :rtype:          list
    	"""
        # TODO: Add optional pin parameter
        return SPI.command(CMD_CAP_GPIOREAD)

    def write_gpio(self, gpio, data):
        """
        Set GPIO channel value.

        :param int gpio:   gpio channel
        :param int data:   data to write to gpio channel.
        """
        bitmask = 1 << gpio
        setclr = 1 if data else 0
        SPI.command(CMD_CAP_GPIOWRITE, params=[bitmask, setclr])
