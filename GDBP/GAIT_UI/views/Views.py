from enum import Enum
from views.login_view import LoginView
from views.home_view import HomeView
from views.connect_view import ConnectView
from views.live_view import LiveView
from views.upload_view import UploadView
from views.history_view import HistoryView
from views.device_view import DeviceView
from views.account_view import AccountView


class Views(Enum):
    LOGIN = 1
    HOME = 2
    CONNECT = 3
    LIVE = 4
    UPLOAD = 5
    HISTORY = 6
    DEVICE = 7
    ACCOUNT = 8

    @staticmethod
    def get_type(view):
        if type(view) is LoginView:
            return Views.LOGIN.value
        elif type(view) is HomeView:
            return Views.HOME.value
        elif type(view) is ConnectView:
            return Views.CONNECT.value
        elif type(view) is LiveView:
            return Views.LIVE.value
        elif type(view) is UploadView:
            return Views.UPLOAD.value
        elif type(view) is HistoryView:
            return Views.HISTORY.value
        elif type(view) is DeviceView:
            return Views.DEVICE.value
        elif type(view) is AccountView:
            return Views.ACCOUNT.value
        else:
            return -1
