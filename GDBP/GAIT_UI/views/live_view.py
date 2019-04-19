from PyQt5.QtWidgets import QWidget
from views.ui_files.live_view_ui import Ui_LiveView
from application.Logger import Logger


class LiveView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_LiveView()
        self._ui.setupUi(self)
        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

