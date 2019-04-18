from PyQt5.QtWidgets import QWidget
from views.ui_files.history_view_ui import Ui_HistoryView


class HistoryView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_HistoryView()
        self._ui.setupUi(self)

