import numpy as np
class DataProcessors:
    def __init__(self):
        None


    @staticmethod
    def bytearray_to_int(array): #, total_bytes, total_samples):
        total_bytes = len(array[0])
        total_samples = int(total_bytes / 4)
        converted_array = []
        for packet in array:

            parsed = [int.from_bytes(packet[i:i + 3], byteorder='little', signed=True) / 1000.0 for i in range(0, total_bytes, 4)]
            parsed_split = [parsed[i:i + 6] for i in range(0, total_samples, 6)]
            converted_array.extend(parsed_split)
        return converted_array