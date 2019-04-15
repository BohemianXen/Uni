from PyQt5.QtWidgets import QMainWindow
from views.main_view_ui import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

    def load_views(self, views):
        tab_layouts = [self._ui.homeGridLayout, self._ui.connectGridLayout, self._ui.liveGridLayout,
                       self._ui.uploadGridLayout,self._ui.historyGridLayout,
                       self._ui.deviceGridLayout, self._ui.accountGridLayout]
        count = 0
        for view in views:
            tab_layouts[count].addWidget(view)
            count += 1

    # update view
    def set_view(self, view):
        self._ui.viewsTabWidget.setCurrentWidget(view)  # TODO: update to match new tab functionality

    def update_home_view(self, view):
        # self._ui.homeGridLayout.removeWidget(self._controller._views['login'])
        # self._ui.homeGridLayout.update()
        self._ui.homeGridLayout.addWidget(view)
