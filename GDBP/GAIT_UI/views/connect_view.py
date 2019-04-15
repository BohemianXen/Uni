from PyQt5.QtWidgets import QWidget
from views.connect_view_ui import Ui_ConnectView


class ConnectView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_ConnectView()
        self._ui.setupUi(self)

