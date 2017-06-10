from opsoro.hardware.spi import SPI

# > I2C                      IN  OUT
CMD_I2C_DETECT      = 20  # 1   1    Test if there's a device at addr
CMD_I2C_READ8       = 21  # 2   1    Read byte
CMD_I2C_WRITE8      = 22  # 3   0    Write byte
CMD_I2C_READ16      = 23  # 2   2    Read 2 bytes
CMD_I2C_WRITE16     = 24  # 4   0    Write 2 bytes


class I2C(object):
    # > I2C
    def detect(self, addr):
        """
        Returns True if an I2C device is found at a particular address.

        :param int addr:   address of the I2C device.

        :return:         I2C device detected
        :rtype:          bool
        """
        return SPI.command(CMD_I2C_DETECT, params=[addr], returned=1)[0] == 1

    def read8(self, addr, reg):
        """
        Read a Byte from an I2C device.

        :param int addr:    address of the I2C device.
        :param int reg:     register address in the I2C device

        :return:         what is the function returning?
        :rtype:          var
        """
        return SPI.command(CMD_I2C_READ8, params=[addr, reg], returned=1)[0]

    def write8(self, addr, reg, data):
        """
        Write a Byte to an I2C device.

        :param int addr:    address of the I2C device.
        :param int reg:     register address in the I2C device
        :param var data:    Byte to send
        """
        SPI.command(CMD_I2C_WRITE8, params=[addr, reg, data])

    def read16(self, addr, reg):
        """
        Read 2 bytes from an I2C device.

        :param int addr:    address of the I2C device.
        :param int reg:     register address in the I2C device

        :return:         2 Bytes
        :rtype:          var
        """
        data = SPI.command(CMD_I2C_READ16, params=[addr, reg], returned=2)
        return (data[0] << 8) | data[1]

    def write16(self, addr, reg, data):
        """
        Write 2 bytes to an I2C device.

        :param int addr:    address of the I2C device.
        :param int reg:     register address in the I2C device
        :param var data:    Bytes to send
        """
        val1 = (data & 0xFF00) >> 8
        val2 = (data & 0x00FF)

        SPI.command(CMD_I2C_WRITE16, params=[addr, reg, val1, val2])
