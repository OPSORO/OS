from opsoro.hardware.spi import SPI

# > SERVO                    IN  OUT
CMD_SERVO_INIT = 40  # 0   0    Init PCA9685
CMD_SERVO_ENABLE = 41  # 0   0    Turn on MOSFET
CMD_SERVO_DISABLE = 42  # 0   0    Turn off MOSFET
CMD_SERVO_NEUTRAL = 43  # 0   0    Set all servos to 1500
CMD_SERVO_SET = 44  # 3   0    Set 1 servo position
CMD_SERVO_SETALL = 45  # 32  0    Set  position of all servos


class Servo(object):
    # > SERVO
    def init(self):
        """Set up the PCA9685 for driving servos."""
        SPI.command(CMD_SERVO_INIT, delay=0.02)

    def enable(self):
        """Turns on the servo power MOSFET, enabling all servos."""
        SPI.command(CMD_SERVO_ENABLE)

    def disable(self):
        """Turns off the servo power MOSFET, disabling all servos."""
        SPI.command(CMD_SERVO_DISABLE)

    def neutral(self):
        """Set all servos to 1500us."""
        SPI.command(CMD_SERVO_NEUTRAL, delay=0.008)

    def set(self, channel, pos):
        """
        Set the position of one servo.
        Pos in us, 500 to 2500

        :param int channel: channel of the servo
        :param int pos:     position of the servo (500 to 2500)
        """
        offtime = (pos + 2) // 4
        SPI.command(CMD_SERVO_SET, params=[channel, offtime >> 8, offtime & 0x00FF], delay=0.008)

    def set_all_us(self, us):
        """
        Set all servos to a certain position (us)

        :param int us:   position in us
        """
        if us == 1500:
            neutral()
        else:
            pos_list = [us for i in range(16)]
            self.set_all(pos_list)

    def set_all(self, pos_list):
        """
        Set position of all 16 servos using a list.

        :param list pos_list:   list of servo positions
        """
        spi_params = []
        i = 0
        for pos in pos_list:
            if pos is None:
                # Tell FW not to update this servo
                spi_params.append(0xFF)
                spi_params.append(0xFF)
            else:
                offtime = (pos + 2) // 4
                spi_params.append(offtime >> 8)
                spi_params.append(offtime & 0x0FF)
            i = i + 1

        SPI.command(CMD_SERVO_SETALL, params=spi_params, delay=0.008)
