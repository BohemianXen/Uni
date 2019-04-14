from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
# from views.main_view import MainView
from views.home_view_ui import Ui_HomeView


class HomeView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_HomeView()
        self._ui.setupUi(self)

