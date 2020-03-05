from Logger import Logger
from PyQt5.QtCore import QRunnable
import winsound
from time import sleep


class AudioPlayer(QRunnable):
    def __init__(self, freq=3000, length=2900):
        super(AudioPlayer, self).__init__()
        self.freq = freq
        self.length = length

    def play(self):
        print('Beep')
        try:
            winsound.Beep(self.freq, self.length)
        except RuntimeError as e:
            print('Could not play audio\n', e)

    def run(self) -> None:
        print('Beep')
        try:
            winsound.Beep(self.freq, self.length)
        except RuntimeError as e:
            print('Could not play audio\n', e)
