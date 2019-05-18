from application.Logger import Logger
from datetime import datetime
from itertools import product


class Converters:
    """ Class for static GAIT data conversion methods.

        Parameters:
            name (str): The name of this class name.
            logger (Logger): Logging instance for this class.
        """

    def __init__(self):
        self.name = self.__class__.name
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
    def bytes_to_int(word, signed):
        """Converts 16-bit words into integers.
        Args:
            word (bytearray): A big-endian array of of 2 bytes.
            signed (bool): Whether or not the input word is signed.

        Returns:
            int: An integer representation of the input.
        """
        return int.from_bytes(word, byteorder='big', signed=signed)

    @staticmethod
    def bcd_to_bytes(bcd):
        """Converts Binary Coded byte to integer.

        Args:
            bcd (bytearray): A BCD byte.

        Returns:
            bytes: The input byte as a bytes object.
        """
        # TODO: Checks for valid BCD (i.e. no chars)
        return bytes([bcd])


    @staticmethod
    def bytes_to_datetime(pairs):
        """Extracts timestamp data from an array of 3 16-bit words.

        Args:
            pairs (tuple): Tuple of RTC data in three bytearray-pairs.

        Returns:
            datetime: Converted date.
        """
        date_string = ''

        # cycle through the major, minor time pairs
        for maj, min in pairs:
            maj, min = hex(maj)[2:], hex(min)[2:]  # convert into hex string and remove 0x prefix

            # zero pad if only one digit then append to date string
            maj_pad = '0' if int(maj) < 10 else ''
            min_pad = '0' if int(min) < 10 else ''
            date_string += maj_pad + maj + ' ' + min_pad + min + ' '

        return datetime.strptime(date_string, '%y %m %d %H %M %S ')


class Tests:
    """ Test class. Tests for the GAIT data conversion methods.

        Parameters:
            name (str): The name of this class name.
            logger (Logger): Logging instance for this class.
        """

    def __init__(self):
        self.name = self.__class__
        self._logger = Logger(self.name)

    @staticmethod
    def test_dates():
        """Tests all possible RTC dates within a century."""
        years = range(100)
        months = range(1, 13)
        dates = range(1, 32)
        hours = range(24)
        mins, secs = range(60), range(60)
        all_permutations = product(years, months, dates, hours, mins, secs)
        for perm in all_permutations:
            year = Converters.bcd_to_bytes(perm[0])
            month = Converters.bcd_to_bytes(perm[1])
            date = Converters.bcd_to_bytes(perm[2])
            hour = Converters.bcd_to_bytes(perm[3])
            mins = Converters.bcd_to_bytes(perm[4])
            secs = Converters.bcd_to_bytes(perm[5])

            year_month = Converters.combine_bytes(year, month)
            date_hour = Converters.combine_bytes(date, hour)
            mins_secs = Converters.combine_bytes(mins, secs)

            result = Converters.bytes_to_datetime((year_month, date_hour, mins_secs))
            print(result)
        None

    @staticmethod
    def test_int_conversions(signed):
        """Tests all possible 16-bit int conversions.

        Args:
            signed (bool): Whether the 16-bit value is signed.

        Returns:
            bool: Test result.
        """
        test = 0
        for i in product(range(256), range(256)):
            two_bytes = Converters.combine_bytes(bytes([i[0]]), bytes([i[1]]))
            result = Converters.bytes_to_int(two_bytes, signed=signed)

            if False and result != test:
                return False

            test += 1
            if test == 32768 and signed:
                test *= -1

        return True


if __name__ == '__main__':
    # TODO: Sanity checks
    # test combine bytes
    test1 = (bytes([255]), bytes([10]))
    result1 = Converters.combine_bytes(test1[0], test1[1])
    print(result1)  # expecting ascii 0xff0a (ff and ascii newline char)

    # test timestamps
    year = Converters.bcd_to_bytes(0b00011001)  # test year is 19 (2019)
    month = Converters.bcd_to_bytes(0b00000101)  # test month is 05 (May)
    date = Converters.bcd_to_bytes(0b00011000)  # test date is 18 (18th)
    hour = Converters.bcd_to_bytes(0b00010101)  # test hour is 17 (17)
    mins = Converters.bcd_to_bytes(0b00100001)  # test mins is 21 (21)
    secs = Converters.bcd_to_bytes(0b00000000)  # test secs is 00 (00)
    print(year, month, date, hour, mins, secs)

    year_month = Converters.combine_bytes(year, month)
    date_hour = Converters.combine_bytes(date, hour)
    mins_secs = Converters.combine_bytes(mins, secs)
    print(year_month, date_hour, mins_secs)

    result2 = Converters.bytes_to_datetime((year_month, date_hour, mins_secs))
    print(type(result2))
    print(result2)

    # test uint conversions
    result3 = Tests.test_int_conversions(signed=False)
    result4 = Tests.test_int_conversions(signed=True)
    print(result3, result4)



