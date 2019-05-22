from PyQt5.QtCore import QObject, pyqtSlot, QThreadPool, QCoreApplication
from application.Logger import Logger


class MainController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model
        self._main_view = None
        self.name = __class__.__name__
        self._logger = Logger(self.name)

    def link_view(self, view):
        self._main_view = view

    # populate linked views and controllers into respective dictionaries for easy central manipulation here in main
    def add_child(self, _type, child, instance):
        _dictionary = self._model.controllers if _type == 'controller' else self._model.views
        _dictionary[child] = instance

    # listeners for view navigation signals
    def establish_listeners(self):
        self._model.controllers['login'].loginComplete.connect(self.set_current_view)

        # search for devices in background on completion of log in
        self._model.controllers['login'].loginComplete.connect(self._model.controllers['connect'].search_button_clicked)

        # home page navigation change slots
        self._model.controllers['home'].connectClicked.connect(self.set_current_view)
        self._model.controllers['home'].liveClicked.connect(self.set_current_view)
        self._model.controllers['home'].uploadClicked.connect(self.set_current_view)
        self._model.controllers['home'].historyClicked.connect(self.set_current_view)
        self._model.controllers['home'].deviceClicked.connect(self.set_current_view)
        self._model.controllers['home'].accountClicked.connect(self.set_current_view)
        self._model.controllers['connect'].connectionComplete.connect(self.unlock_views)

    @pyqtSlot(str)
    def set_current_view(self, view):
        """Changes the currently active view.

        Args:
            view (str): The name of the view that needs to be switch to.
       """
        self._logger.log('Requesting view change', Logger.INFO)

        # first navigation from login to home is unique, else switch to selected tab
        if view == 'home_first':
            self._main_view.update_main_view()
            view = 'home'

        self._main_view.set_view(self._model.views[view])
        self._logger.log('View change completed', Logger.INFO)

    @pyqtSlot(bool)
    def unlock_views(self, complete):
        for name, controller in self._model.controllers.items():
            if complete and name == 'live':  # and name == 'upload':
                controller.unlock_view()

    @staticmethod
    def on_close():
        """Called on app close. Attempts to ensure all threads are closed before closing."""
        pools = QThreadPool.globalInstance()
        print('{} thread(s) were running on termination'.format(pools.activeThreadCount()))
        while pools.activeThreadCount() > 0:
            pools.waitForDone(3000)
            print('Finishing up...')

        QCoreApplication.exit(0)
