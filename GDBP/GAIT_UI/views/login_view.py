from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
# from views.main_view import MainView
from views.login_view_ui import Ui_LoginView


class LoginView(QWidget):
    def __init__(self, login_controller):
        super().__init__()

        self._login_controller = login_controller
        self._ui = Ui_LoginView()
        self._ui.setupUi(self)

