from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


# TODO: Field checks
class LoginController(QObject):

    # signals for view navigation that are handled by main controller
    loginComplete = pyqtSignal(str)

    def __init__(self, model):
        super().__init__()

        self._model = model
        self._view = None

        # slot connecting for response to model signals
        self._model.usernameExists.connect(self.check_password)

    def link_view(self, view):
        self._view = view

    # slot implementations for model signals
    @pyqtSlot()
    def login_clicked(self):
        print("Login Pressed!")
        self._model.find_username(self._view.get_username())

    @pyqtSlot()
    def check_password(self):
        password = self._model.get_password(self._view.get_username())
        print("Password \"" + password + "\" entered")
        if password == "password":
            print("Password OK")
            self.loginComplete.emit('home_first')
