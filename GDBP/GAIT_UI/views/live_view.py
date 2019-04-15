from PyQt5.QtWidgets import QWidget
from views.live_view_ui import Ui_LiveView


class LiveView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_LiveView()
        self._ui.setupUi(self)

