import sys
from application.Logger import Logger
from PyQt5.QtWidgets import QApplication

# import models
from models.main_model import MainModel
from models.login_model import LoginModel
from models.home_model import HomeModel
from models.connect_model import ConnectModel
from models.live_model import LiveModel
from models.upload_model import UploadModel
from models.history_model import HistoryModel
from models.device_model import DeviceModel
from models.account_model import AccountModel

# import views
from views.main_view import MainView
from views.login_view import LoginView
from views.home_view import HomeView
from views.connect_view import ConnectView
from views.live_view import LiveView
from views.upload_view import UploadView
from views.history_view import HistoryView
from views.device_view import DeviceView
from views.account_view import AccountView


# import controllers
from controllers.main_controller import MainController
from controllers.login_controller import LoginController
from controllers.home_controller import HomeController
from controllers.connect_controller import ConnectController
from controllers.live_controller import LiveController
from controllers.upload_controller import UploadController
from controllers.history_controller import HistoryController
from controllers.device_controller import DeviceController
from controllers.account_controller import AccountController


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.setStyle('Fusion')
        self.name = self.__class__.__name__
        self.logger = Logger(self.name)
        self.logger.log('App started', self.logger.INFO)

        # list of all modules
        self.module_names = ['login', 'home', 'connect', 'live', 'upload', 'history', 'device', 'account']
        self.instantiate_framework()
        self.link_controllers_to_views()
        self.establish_hierarchies()
        self.load_views()

    # create model, view, and controller instances
    def instantiate_framework(self):
        # instantiate models
        self.logger.log('Instantiating models', self.logger.INFO)
        self.main_model = MainModel()
        self.login_model = LoginModel()
        self.home_model = HomeModel()
        self.connect_model = ConnectModel()
        self.live_model = LiveModel()
        self.upload_model = UploadModel()
        self.history_model = HistoryModel()
        self.device_model = DeviceModel()
        self.account_model = AccountModel()

        # instantiate controllers and link them to their respective models
        self.logger.log('Instantiating controllers', self.logger.INFO)
        self.main_controller = MainController(self.main_model)
        self.login_controller = LoginController(self.login_model)
        self.home_controller = HomeController(self.home_model)
        self.connect_controller = ConnectController(self.connect_model)
        self.live_controller = LiveController(self.live_model)
        self.upload_controller = UploadController(self.upload_model)
        self.history_controller = HistoryController(self.history_model)
        self.device_controller = DeviceController(self.device_model)
        self.account_controller = AccountController(self.account_model)

        # instantiate views and link them to their respective controllers
        self.logger.log('Instantiating views', self.logger.INFO)
        self.main_view = MainView(self.main_controller)
        self.login_view = LoginView(self.login_controller)
        self.home_view = HomeView(self.home_controller)
        self.connect_view = ConnectView(self.connect_controller)
        self.live_view = LiveView(self.live_controller)
        self.upload_view = UploadView(self.upload_controller)
        self.history_view = HistoryView(self.history_controller)
        self.device_view = DeviceView(self.device_controller)
        self.account_view = AccountView(self.account_controller)

    def link_controllers_to_views(self):
        self.logger.log('Linking controllers to views', self.logger.INFO)
        self.main_controller.link_view(self.main_view)
        self.login_controller.link_view(self.login_view)
        self.connect_controller.link_view(self.connect_view)
        self.live_controller.link_view(self.live_view)
        self.upload_controller.link_view(self.upload_view)
        self.history_controller.link_view(self.history_view)
        self.device_controller.link_view(self.device_view)
        self.account_controller.link_view(self.account_view)

    # make all controllers children of main
    def establish_hierarchies(self):
        self.controllers = [self.login_controller, self.home_controller, self.connect_controller, self.live_controller,
                            self.upload_controller, self.history_controller, self.device_controller,
                            self.account_controller]

        self.views = [self.login_view, self.home_view, self.connect_view, self.live_view, self.upload_view,
                      self.history_view, self.device_view, self.account_view]

        self.logger.log('Configuring main controller', self.logger.INFO)
        count = 0
        for name in self.module_names:
            self.main_controller.add_child('controller', name, self.controllers[count])
            self.main_controller.add_child('view', name, self.views[count])
            count += 1

    def load_views(self):
        self.logger.log('Loading views', self.logger.INFO)
        # load all views into stacked central widget- leaves the login view as active
        self.views.remove(self.login_view)  # true home view is deferred until login is complete
        self.main_view.load_views(self.views)
        self.main_view.add_login_view(self.login_view)
        self.main_controller.establish_listeners()

        # show window and set up listeners for view change triggers
        self.main_view.show()

    def on_close(self):
        self.exec_()
        self.logger.log('App closing', self.logger.INFO)


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.on_close())
