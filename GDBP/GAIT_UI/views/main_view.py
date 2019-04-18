from PyQt5.QtWidgets import QMainWindow
from views.ui_files.main_view_ui import Ui_MainWindow
from views.Views import Views


class MainView(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        # tab indexes
        self._tabs = {
            '2': self._ui.homeTab,
            '3': self._ui.connectTab,
            '4': self._ui.liveTab,
            '5': self._ui.uploadTab,
            '6': self._ui.historyTab,
            '7': self._ui.deviceTab,
            '8': self._ui.accountTab
        }

    # adds all views to their respective grid layouts as children
    def load_views(self, views):
        tab_layouts = [self._ui.homeGridLayout, self._ui.connectGridLayout, self._ui.liveGridLayout,
                       self._ui.uploadGridLayout, self._ui.historyGridLayout,
                       self._ui.deviceGridLayout, self._ui.accountGridLayout]
        count = 0
        for view in views:
            tab_layouts[count].addWidget(view)
            count += 1

    # update current tab
    def set_view(self, view):
        self._ui.viewsTabWidget.setCurrentWidget(self._tabs[str(Views.get_type(view))])

    # update home view when first logging in
    def update_home_view(self, view):
        # self._ui.homeGridLayout.removeWidget(self._controller._views['login'])
        # self._ui.homeGridLayout.update()
        self._ui.homeGridLayout.addWidget(view)
