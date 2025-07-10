from backend.imports import *

class DashboardWindow(object):
    def setupUi(self, Widget):
        Widget.setObjectName("DashboardWindow")
        Widget.resize(600, 400)

        if isinstance(Widget, QMainWindow):
            self.container = QWidget()
            self.layout = QVBoxLayout(self.container)
            Widget.setCentralWidget(self.container)
        else:
            self.layout = QVBoxLayout(Widget)

        self.label = QLabel("Welcome to the Dashboard!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font: 700 20pt 'Meiryo UI';")

        self.layout.addWidget(self.label)