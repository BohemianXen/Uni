from PyQt5.QtCore import QObject, pyqtSignal
from application.Logger import Logger
from models.Database import Database
from PyQt5.QtSql import QSqlQuery


class LoginModel(QObject):
    """ Model class. Holds program data and the interfaces that allow for the values to be obtained/updated.

    Parameters:
        userNameExists (pyqtSignal): Signal emitted when a matching username is found.
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
        _db (Database): Database connection instance for this class.
        _query(QSqlQuery): Gateway for any database queries.
    """

    usernameExists = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        self._db = Database(self.name)  # database connection instance
        self._query = QSqlQuery(self._db.db)  # database query gateway for instance

    def find_username(self, username):
        """Attempts to find a matching username in the database."""
        # TODO: attempts, check not null, poop
        self._logger.log("Searching db for user {}".format(username), Logger.DEBUG)
        found = False

        try:
            self._query.prepare('SELECT id, username, password FROM accounts WHERE accounts.username = ?')
            self._query.addBindValue(username)
            query_successful = self._query.exec()

            if query_successful:
                found = True if self._query.first() else False

        except Exception as e:
            self._logger.log("Error querying database: {}".format(e), Logger.ERROR)
            self._logger.log(self._query.lastError().text(), Logger.DEBUG)

        if not found:
            self._logger.log("Username: {} not found".format(username, found), Logger.DEBUG)

        self.usernameExists.emit(found)

    def get_password(self):
        """Gets the password in the queried record. Only called after username is found.

        Returns:
            string: The user's password.
        """
        return self._query.value(2)

    def close(self):
        """Closes the database connection."""
        self._db.close()
