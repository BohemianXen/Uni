from PyQt5.QtWidgets import QMainWindow, QStyleFactory
from views.ui_files.main_view_ui import Ui_MainWindow
from views.Views import Views
from application.Logger import Logger


class MainView(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

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
        new_view = self._tabs[str(Views.get_type(view))]
        current_view_name = self._ui.viewsTabWidget.currentWidget().objectName()
        self._logger.log('Changing from {} to {}'.format(current_view_name, new_view.objectName()), self._logger.INFO)

        try:
            self._ui.viewsTabWidget.setCurrentWidget(new_view)
        except:
            self._logger.log('Error changing to {} view'.format(new_view), self._logger.ERROR)

    def add_login_view(self, view):
        self._ui.mainStackedWidget.addWidget(view)
        self._ui.mainStackedWidget.setCurrentWidget(view)

    # update main view when first logging in
    def update_main_view(self):
        self._logger.log('Changing loginView to homeView on mainTab', self._logger.INFO)
        self._ui.mainStackedWidget.setCurrentWidget(self._ui.loggedInView)
