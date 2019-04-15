from PyQt5.QtCore import QObject, pyqtSlot


class MainController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model
        self._main_view = None

        self._views = {
            'login': None,
            'home': None
        }
        self._controllers = self._views.copy()

    def link_view(self, view):
        self._main_view = view

    def add_child(self, _type, child, instance):
        _dictionary = self._controllers if _type == 'controller' else self._views
        _dictionary[child] = instance

    # listeners for view switch events
    def establish_listeners(self):
        self._controllers['login'].login_complete.connect(self.set_current_view)

    # update view on signal trigger
    @pyqtSlot(str)
    def set_current_view(self, view):
        if view == 'home_first':
            self._views['login'].hide()
            self._main_view.update_home_view(self._views['home'])
        else:
            self._main_view.set_view(self._views[view])
