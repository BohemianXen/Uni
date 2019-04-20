from PyQt5.QtWidgets import QWidget
from views.ui_files.account_view_ui import Ui_AccountView
from application.Logger import Logger


class AccountView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_AccountView()
        self._ui.setupUi(self)

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

    # move to logged in view since log in complete
    def unlock_view(self):
        self._logger.log('Unlocking {}'.format(self.name), self._logger.INFO)
        self._ui.accountStackedWidget.setCurrentWidget(self._ui.loggedInView)

