from PyQt5.QtCore import QObject, pyqtSlot


class MainController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model
        self._main_view = None

        self._views = {
            'login': None,
            'home': None,
            'connect': None,
            'live': None,
            'upload': None,
            'history': None,
            'device': None,
            'account': None
        }
        self._controllers = self._views.copy()

    def link_view(self, view):
        self._main_view = view

    # populate linked views and controllers into respective dictionaries for easy central manipulation here in main
    def add_child(self, _type, child, instance):
        _dictionary = self._controllers if _type == 'controller' else self._views
        _dictionary[child] = instance

    # listeners for view navigation signals
    def establish_listeners(self):
        self._controllers['login'].loginComplete.connect(self.set_current_view)
        self._controllers['home'].connectClicked.connect(self.set_current_view)
        self._controllers['home'].liveClicked.connect(self.set_current_view)
        self._controllers['home'].uploadClicked.connect(self.set_current_view)
        self._controllers['home'].historyClicked.connect(self.set_current_view)
        self._controllers['home'].deviceClicked.connect(self.set_current_view)
        self._controllers['home'].accountClicked.connect(self.set_current_view)

    # update view on navigation triggers
    @pyqtSlot(str)
    def set_current_view(self, view):
        # first navigation from login to home is unique, else switch to selected tab
        if view == 'home_first':
            self._views['login'].hide()
            self._main_view.update_home_view(self._views['home'])
        else:
            self._main_view.set_view(self._views[view])
