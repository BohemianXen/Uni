import sys
from PyQt5.QtWidgets import QApplication
from views.main_view import MainView
from views.login_view import LoginView
from models.main_model import MainModel
from models.login_model import LoginModel
from controllers.main_controller import MainController
from controllers.login_controller import LoginController


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.main_model = MainModel()
        self.login_model = LoginModel()
        self.main_controller = MainController(self.main_model)
        self.login_controller = LoginController(self.login_model)

        views = []
        self.main_view = MainView(self.main_controller)
        self.login_view = LoginView(self.login_controller)

        views.append(self.login_view)
        self.main_view.load_views(views)
        self.main_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())

