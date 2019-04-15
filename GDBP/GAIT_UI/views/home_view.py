from PyQt5.QtWidgets import QWidget
from views.home_view_ui import Ui_HomeView


class HomeView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_HomeView()
        self._ui.setupUi(self)

        self._ui.connectPushButton.clicked.connect(lambda: self._controller.connect_clicked())
        self._ui.livePushButton.clicked.connect(lambda: self._controller.live_clicked())
        self._ui.uploadPushButton.clicked.connect(lambda: self._controller.upload_clicked())
        self._ui.historyPushButton.clicked.connect(lambda: self._controller.history_clicked())
        self._ui.devicePushButton.clicked.connect(lambda: self._controller.device_clicked())
        self._ui.accountPushButton.clicked.connect(lambda: self._controller.account_clicked())


