from PyQt5.QtCore import QObject, pyqtSlot, QThreadPool
from application.Logger import Logger
from controllers.live_manager.PortTest import PortTest
from controllers.live_manager.LiveMotion import LiveMotion


class LiveController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model
        self._view = None

        self.name = __class__.__name__
        self._logger = Logger(self.name)

        self.pool = QThreadPool.globalInstance()

        self.plotting = False
        self.live_motion = None

        self.host = ''
        self.port = ''
        self.uuid = 0x1200

    def link_view(self, view):
        self._view = view

    # update view following connect event
    def unlock_view(self):
        self._view.unlock_view()
        # self.start_test()

    def button_toggled(self, view_type):
        if self.plotting:
            self.stop_plotting()

        self._view.change_stacked_widget(view_type)

    def start_test(self):
        port_test = PortTest(self.host, self.port, self.uuid)
        port_test.signals.testComplete.connect(self.test_complete)
        self.pool.start(port_test)

    def update_test_console(self, message):
        self._view.update_test_console(message)

    @pyqtSlot(str)
    def start_plot(self, data_type):
        self.plotting = True

        if data_type == 'motion':
            self._logger.log('Starting live motion plot', Logger.DEBUG)
            live_motion = LiveMotion()
            live_motion.signals.dataReady.connect(self.update_plot)
            self.pool.start(live_motion)
            self.live_motion = live_motion

    @pyqtSlot(str, float)
    def update_plot(self, data_type, data):
        if data_type == 'motion':
            self._model.add_motion_data(data)
            self._view.update_motion_plot(self._model.motion_data)

    def stop_plotting(self):
        self._logger.log('Stopping plot', Logger.DEBUG)

        if self.live_motion is not None:
            self.live_motion.plotting = False
            self.live_motion = None

        self._model.reset_data()
        self.plotting = False
