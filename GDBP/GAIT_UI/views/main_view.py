from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from views.main_view_ui import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

    def load_views(self, views):
        for view in views:
            self._ui.views.addWidget(view)

    def set_view(self, view):
        self._ui.views.setCurrentWidget(view)
