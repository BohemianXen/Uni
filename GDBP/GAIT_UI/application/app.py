import sys
from PyQt5.QtWidgets import QApplication

# import models
from models.main_model import MainModel
from models.login_model import LoginModel
from models.home_model import HomeModel

# import views
from views.main_view import MainView
from views.login_view import LoginView
from views.home_view import HomeView

# import controllers
from controllers.main_controller import MainController
from controllers.login_controller import LoginController
from controllers.home_controller import HomeController

class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        # instantiate models
        self.main_model = MainModel()
        self.login_model = LoginModel()
        self.home_model = HomeModel()

        # instantiate controllers and link them to their respective models
        self.main_controller = MainController(self.main_model)
        self.login_controller = LoginController(self.login_model)
        self.home_controller = HomeController(self.home_model)

        # instantiate views and link them to their respective controllers
        self.main_view = MainView(self.main_controller)
        self.login_view = LoginView(self.login_controller)
        self.home_view = HomeView(self.home_controller)

        # load all views into stacked central widget- sets the log-in view as active
        views = [self.login_view, self.home_view]
        # views.append(self.login_view)
        self.main_view.load_views(views)
        self.main_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())

