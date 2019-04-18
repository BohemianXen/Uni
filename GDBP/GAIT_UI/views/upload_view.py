from PyQt5.QtWidgets import QWidget
from views.ui_files.upload_view_ui import Ui_UploadView


class UploadView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._ui = Ui_UploadView()
        self._ui.setupUi(self)

