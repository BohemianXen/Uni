from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from views.ui_files.login_view_ui import Ui_LoginView
from application.Logger import Logger


class LoginView(QWidget):
    """ View class. Instantiates all UI QWidgets associated with this view and links signals to controller slots.

    Args:
        controller (QWidget): The view's corresponding controller; that which manipulates this view.

    Parameters:
        _controller (QWidget): A reference to the passed controller.
        _ui (Ui_LiveView): Holds all the generated UI elements for an added layer of abstraction.
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
    """

    def __init__(self, controller):
        super().__init__()
        self._controller = controller
        self._ui = Ui_LoginView()
        self._ui.setupUi(self)

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        self._ui.incorrectLabel.setVisible(False)  # TODO: use signals and slots

        # connect login button click event to its slot
        self._ui.loginPushButton.clicked.connect(lambda: self._controller.login_button_clicked())

    # link enter/return key events to login_clicked handler; overrides QtWidget event handler
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
            self._controller.login_button_clicked()

    # returns the username entered by the user
    def get_username(self):
        return self._ui.usernameLineEdit.text()

    # returns the plaintext password entered by the user
    def get_password(self):
        return self._ui.passwordLineEdit.text()
