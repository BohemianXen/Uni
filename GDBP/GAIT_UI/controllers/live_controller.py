from PyQt5.QtCore import QObject, pyqtSlot
from application.Logger import Logger
from controllers.live_manager.PortTest import PortTest


class LiveController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model
        self._view = None

        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.host = ''
        self. port = ''
        self.uuid = 0x1200

    def link_view(self, view):
        self._view = view

    # update view following connect event
    def unlock_view(self):
        self._view.unlock_view()
        # self.start_test()

    def button_toggled(self, view_type):
        self._view.change_stacked_widget(view_type)

    def start_test(self):
        port_test = PortTest(self.host, self.port, self.uuid)
        port_test.signals.testComplete.connect(self.test_complete)
        self.pool.start(port_test)

    def update_test_console(self, message):
        self._view.update_test_console(message)