from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class Dashboard(QMainWindow):
    def __init__(self):
        super(Dashboard, self).__init__()
        uic.loadUi('ui/dashboard.ui', self)  # Load the dashboard UI
        self.showMaximized()
