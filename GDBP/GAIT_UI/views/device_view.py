from PyQt5.QtWidgets import QWidget
from views.ui_files.device_view_ui import Ui_DeviceView
from application.Logger import Logger


class DeviceView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_DeviceView()
        self._ui.setupUi(self)

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)
