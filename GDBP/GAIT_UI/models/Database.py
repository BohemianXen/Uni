from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtCore import QObject
from application.Logger import Logger


class Database(QObject):
    """ Model class. Holds program data and the interfaces that allow for the values to be obtained/updated.

    Parameters:
        parent(string): Name of the model that's creating the connection.
        name (str): The name of this class name.
        logger (Logger): Logging instance for this class.
    """

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        self._logger.log('Creating connection for {}'.format(self.parent), Logger.DEBUG)

        # create a database instance using the demo account
        self.db = QSqlDatabase('QMYSQL')
        self.db.setHostName('localhost')
        self.db.setPort(3306)
        self.db.setUserName('GAIT')
        self.db.setPassword('GAIT123')
        self.db.setDatabaseName('demo_app')

        self.connection_open = self.db.open()
        if not self.connection_open:
            self._logger.log('Connection creation for {} failed {}', Logger.DEBUG)
            self.db = None

    def close(self):
        """Safely closes the connection (if open)."""
        if self.connection_open:
            self._logger.log('Closing database connect for {}'.format(self.parent), Logger.DEBUG)
            self.db.close()
