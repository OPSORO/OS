from opsoro.hardware.spi import SPI


# > ANALOG                   IN  OUT
CMD_ANA_GET         = 100  # 1   2    Read an analog channel
CMD_ANA_GETALL      = 101  # 0   8    Read all analog channels

class Analog(object):
    # > ANALOG
    def read_channel(self, channel):
        """
        Reads the value of a single analog channel.

        :param int channel:     analog channel to read

        :return:         analog value of the channel
        :rtype:          var
        """
        data = SPI.command(CMD_ANA_GET, params=[channel], returned=2)
        return data[0] << 8 | data[1]

    def read_all_channels(self):
        """
        Reads all analog channels and returns them as a list.

        :return:         analog values
        :rtype:          list
        """
        data = SPI.command(CMD_ANA_GETALL, returned=2)
        return [
            data[0] << 8 | data[1], data[2] << 8 | data[3], data[4] << 8 |
            data[5], data[6] << 8 | data[7]
        ]
