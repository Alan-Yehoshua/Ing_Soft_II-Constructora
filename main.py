from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import sys

class HomeWindow(QMainWindow):
    def __init__(self):
        super(HomeWindow, self).__init__()
        loadUi("HomePage.ui", self)
        
        self.CustomerButton.clicked.connect(self.customerPage)
        self.EmployeButton.clicked.connect(self.employePage)
        
    def customerPage(self):
        self.stackedWidget.setCurrentIndex(0)
        
    def employePage(self):
        self.stackedWidget.setCurrentIndex(1)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = HomeWindow()
    ui.show()
    sys.exit(app.exec_()) 