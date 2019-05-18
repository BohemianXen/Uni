from application.Logger import Logger
from datetime import datetime


class Converters:
    """ Application class. Instantiates all UI models, views, and controllers.

        Args:
            sys_argv (list): Command line arguments for debug purposes.

        Parameters:
            name (str): The name of this class name.
            logger (Logger): Logging instance for this class.
        """

    def __init__(self):
        self.name = __class__
        self._logger = Logger(self.name)

    @staticmethod
    def combine_bytes(msb, lsb):
        """Concatenates two msb, lsb bytes into one 32-bit word.

        Args:
             msb (bytes): The high byte in the packet data field.
             lsb (bytes): The low byte in the packet data field.

         Returns:
             combination (bytearray): A big endian array of the input bytes.
        """
        combination = bytearray(msb)
        combination.extend(lsb)  # append lsb to msb
        return combination

    @staticmethod
    def bytes_to_uint(word):
        """Converts 32-bit words into unsigned integers.
        Args:
            word (bytearray): A big-endian array of of 4 bytes.

        Returns:
             int_val (int): An unsigned integer representation of the input.
        """
        #combination = bytearray(msb)
        #combination.extend(lsb)  # append lsb to msb
        #return combination

    @staticmethod
    def bcd_to_int(chars):
        """Converts Binary Coded Decimals to integers.

        Args:
            chars (bytearray): A big-endian array of bytes.
        """
        for char in chars:
            char = ord(char)
            for val in (char >> 4, char & 0xF):
                if val == 0xF:
                    return
                yield val

    @staticmethod
    def bcd_to_datetime(bcd_date, type):
        """Extracts timestamps data from a 32-bit word.
        """
        int_date = []
        return datetime(int_date)


if __name__ == '__main__':
    converters = Converters()
    test = (bytes([255]), bytes([10]))
    result = converters.combine_bytes(test[0], test[1])
    print(result)

