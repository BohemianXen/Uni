from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from views.ui_files.login_view_ui import Ui_LoginView


class LoginView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_LoginView()
        self._ui.setupUi(self)
        self._ui.incorrectLabel.setVisible(False)  # TODO: use signals and slots

        # connect login button click event to its slot
        self._ui.loginPushButton.clicked.connect(lambda: self._controller.login_clicked())

    # link enter/return key events to login_clicked handler; overrides QtWidget event handler
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
            self._controller.login_clicked()

    # returns the username entered by the user
    def get_username(self):
        return self._ui.usernameLineEdit.text()

    # returns the plaintext password entered by the user
    def get_password(self):
        return self._ui.passwordLineEdit.text()
