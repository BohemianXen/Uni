from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class LoginController(QObject):

    login_complete = pyqtSignal()

    def __init__(self, model):
        super().__init__()

        self._model = model
        self._view = None

        self._model.username_exists.connect(self.check_password)

    def link_view(self, view):
        self._view = view

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
            self.login_complete.emit()
