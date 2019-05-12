from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


# TODO: Field checks
class LoginController(QObject):
    """ Controller class. Handles the core program logic and data transfer between its view and model counterparts.

        Args:
            model (QWidget): The controller's corresponding model.

        Parameters:
            loginComplete (pyqtSignal): Signal emitted when login has been completed.
            _model (QWidget): A reference to the passed model.
            _view (QWidget): A reference to this controller's corresponding view.
        """

    loginComplete = pyqtSignal(str)  # the signal passes the name of the next view when emitted

    def __init__(self, model):
        super().__init__()

        self._model = model
        self._view = None  # set later through the "link_view" method

        # slot connecting for response to model signals
        self._model.usernameExists.connect(self.check_password)

    def link_view(self, view):
        self._view = view

    # slot implementations for view and model signals
    @pyqtSlot()
    def login_button_clicked(self):
        # print("Login Pressed!")
        self._model.find_username(self._view.get_username())

    @pyqtSlot()
    def check_password(self):
        password = self._model.get_password(self._view.get_username())
        # print("Password \"" + password + "\" entered")
        if password == "password":
            # print("Password OK")
            self.loginComplete.emit('home_first')
