from PyQt5.QtCore import QObject, pyqtSignal


class LoginModel(QObject):

    username_exists = pyqtSignal()

    def __init__(self):
        super().__init__()

    def find_username(self, username):
        print("Username OK")
        self.username_exists.emit()

    def get_password(self, username):
        print("Getting Password")
        return "password"



