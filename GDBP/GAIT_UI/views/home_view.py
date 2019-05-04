from PyQt5.QtWidgets import QWidget
from views.ui_files.home_view_ui import Ui_HomeView
from application.Logger import Logger


class HomeView(QWidget):
    """ View class. Instantiates all UI QWidgets associated with this view and links signals to controller slots.

    Args:
        controller (QWidget): The view's corresponding controller; that which manipulates this view.

    Parameters:
        _controller (QWidget): A reference to the passed controller.
        _ui (Ui_LiveView): Holds all the generated UI elements for an added layer of abstraction.
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
    """

    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_HomeView()
        self._ui.setupUi(self)
        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        # connect button click events to their respective slots
        self._ui.connectPushButton.clicked.connect(lambda: self._controller.connect_clicked())
        self._ui.livePushButton.clicked.connect(lambda: self._controller.live_clicked())
        self._ui.uploadPushButton.clicked.connect(lambda: self._controller.upload_clicked())
        self._ui.historyPushButton.clicked.connect(lambda: self._controller.history_clicked())
        self._ui.devicePushButton.clicked.connect(lambda: self._controller.device_clicked())
        self._ui.accountPushButton.clicked.connect(lambda: self._controller.account_clicked())
