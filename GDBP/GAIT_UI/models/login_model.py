from PyQt5.QtCore import QObject, pyqtSignal
from application.Logger import Logger


class LoginModel(QObject):
    """ Model class. Holds program data and the interfaces that allow for the values to be obtained/updated.

    Parameters:
        userNameExists (pyqtSignal): Signal emitted when a matching username is found.
        name (str): The name of this class.
        logger (Logger): Logging instance for this class.
    """

    usernameExists = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

    def find_username(self, username):
        # TODO: Implement database query for passed username.
        self.usernameExists.emit()

    def get_password(self, username):
        # TODO: Implement hashed password retrieval.
        return "password"
