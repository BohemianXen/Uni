from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from views.main_view_ui import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self, main_controller):
        super().__init__()

        self._main_controller = main_controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

    def load_views(self, views):
        for view in views:
            self._ui.views.addWidget(view)
        self._ui.views.setCurrentWidget(views[0])
