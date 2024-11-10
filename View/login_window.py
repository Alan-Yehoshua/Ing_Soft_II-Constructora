from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow

class LogInWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.setup_ui()
        
    def setup_ui(self):
        loadUi("C:/Python_code/Ing_Soft_II_Constrcutora/View/login.ui", self)
        self.showPassword.toggled.connect(self.showPass)
        self.login.clicked.connect(self.login_button_clicked)
        
    def showPass(self, checked):
        if checked:
            self.password.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        
    def login_button_clicked(self):
        if self.controller:
            self.controller.log_in()
        else:
            print("Controlador no asignado.")

    def show_message(self, title, message):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.exec_()