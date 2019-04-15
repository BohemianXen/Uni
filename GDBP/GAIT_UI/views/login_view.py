from PyQt5.QtWidgets import QWidget
from views.login_view_ui import Ui_LoginView


class LoginView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_LoginView()
        self._ui.setupUi(self)
        self._ui.incorrectLabel.setVisible(False)  # TODO: use slots

        self._ui.loginPushButton.clicked.connect(lambda: self._controller.login_clicked())

    def get_username(self):
        return self._ui.usernameLineEdit.text()

    def get_password(self):
        return self._ui.passwordLineEdit.text()
