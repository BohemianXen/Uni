from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from application.Logger import Logger
from hashlib import sha256


# TODO: Field checks
class LoginController(QObject):
    """ Controller class. Handles the core program logic and data transfer between its view and model counterparts.

    Args:
        model (QWidget): The controller's corresponding model.

    Parameters:
        loginComplete (pyqtSignal): Signal emitted when login has been completed.
        _model (QWidget): A reference to the passed model.
        _view (QWidget): A reference to this controller's corresponding view.
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
    """

    loginComplete = pyqtSignal(str)  # the signal passes the name of the next view when emitted

    def __init__(self, model):
        super().__init__()

        self._model = model
        self._view = None  # set later through the "link_view" method

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        # slot connecting for response to model signals
        self._model.usernameExists.connect(self.check_password)

    def link_view(self, view):
        self._view = view

    @pyqtSlot()
    def login_button_clicked(self):
        """Slot implementation for login button click."""
        self._model.find_username(self._view.get_username())

    @pyqtSlot(bool)
    def check_password(self, username_exists):
        """Slot implementation for usernameExists signal."""
        pword_match = False

        if username_exists:
            self._logger.log("Matching username found, checking password", Logger.DEBUG)
            password = self._model.get_password()
            entered_password = sha256(self._view.get_password().encode('utf-8')).hexdigest()
            pword_match = True if password is not None and password == entered_password else False

        if username_exists and pword_match:
            self.loginComplete.emit('home_first')  # go to home page for the first time
            self._view.toggle_incorrect_label(value=False)
        else:
            self._logger.log("Username found - {}, password matched - {}".format(username_exists, pword_match),
                             Logger.DEBUG)
            self._view.toggle_incorrect_label(value=True)
