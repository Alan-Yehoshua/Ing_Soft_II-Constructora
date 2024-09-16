from PyQt5.QtWidgets import QMainWindow, QLineEdit, QMessageBox
from mainwindow import MainWindow
from ui_login import Ui_Login
from supabase import create_client, Client
import sys

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        
        self.messageBox = QMessageBox()
        self.messageBox.setStyleSheet("""
            QMessageBox {
            background-color: #2C3E50;
            }
            QPushButton {
            border-radius: 5px;
            border: 1px solid black;
            background: #ECF0F1;
            width: 55px;
            heigth: 25px;
            color: #BDC3C7;
            font-size: 14px;
            }
            QPushButton:hover {
            background: #7F8C8D;
            }
            QLabel {
            color: #BDC3C7;
            font-size: 14px;
            }
        """)
        
        self.ui.showPassword.toggled.connect(self.showPass)
        self.ui.login.clicked.connect(self.login)
        
    def showPass(self, checked):
        self.ui.password.setEchoMode(QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password)
        
    def login(self):
        password = self.ui.password.text()
        username = self.ui.username.text()
        self.supabase: Client = create_client("https://qlsmhahdkovvqfauntde.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFsc21oYWhka292dnFmYXVudGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYwNjcxMjIsImV4cCI6MjA0MTY0MzEyMn0.K-LSXODTvSbvFqu6hnJWYiP8KDmm959LZB5xYQl6aPI")
        
        if password == "" or username == "":
            self.messageBox.warning(self.messageBox,"Error",
            "Algun campo vacio",
            self.messageBox.StandardButton.Ok,
            self.messageBox.StandardButton.Ok)
        elif password == "12345" and username == "Admin":
            self.close()
            self.goToHomeWindow()
        else:
            # Consulta a la base de datos para verificar las credenciales
            response = self.supabase.from_("empleados").select("*").eq("username", username).eq("password", password).execute()
            
            if response.data:
                # Si las credenciales son correctas
                user_data = response.data[0]  # Obtenemos los datos del usuario
                
                # Verificamos el puesto del usuario
                if user_data['puesto'] == "Administrador":
                    self.close()
                    self.goToHomeWindow()  # Ventana de administrador
                else:
                    self.close()
                    self.goToRegularHomeWindow()  # Ventana normal
            else:
                # Si las credenciales son incorrectas
                self.messageBox.warning(self.messageBox, "Error",
                                         "Credenciales incorrectas",
                                         self.messageBox.StandardButton.Ok,
                                         self.messageBox.StandardButton.Ok)
                
    #FUNCION PARA ABRIR LA VENTANA PRINCIPAL------------------------------------
    def goToHomeWindow(self):
        self.mainwindow = MainWindow()
        self.mainwindow.show()
    #FUNCION PARA ABRIR LA VENTANA PRINCIPAL (usuarios no admin)------------------------------------
    def goToRegularHomeWindow(self):
        # Lógica para abrir la ventana de usuario regular
        self.messageBox.information(self, "Usuario Standar", "Usuario Normal")
