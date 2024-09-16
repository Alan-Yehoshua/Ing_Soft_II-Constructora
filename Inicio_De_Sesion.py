from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCheckBox, QMessageBox
import sys
from supabase import create_client, Client

from main import HomeWindow   

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 565)
        MainWindow.setMinimumSize(QtCore.QSize(450, 565))
        MainWindow.setMaximumSize(QtCore.QSize(450, 565))
        MainWindow.setWindowTitle("Inicio De Sesion")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icon/lightning-bolt-256.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet("QWidget{\n"
                                 "    background: #2C3E50 ;\n"
                                 "    color: #BDC3C7;\n"
                                 "}")
        MainWindow.setIconSize(QtCore.QSize(32, 32))
        self.main_window = MainWindow
        self.LogIn_Window = QtWidgets.QWidget(MainWindow)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.LogIn_Window)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(140, 120, 164, 271))
        self.Layout_Login = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.Layout_Login.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.Layout_Login.setContentsMargins(10, 25, 10, 25)
        self.Layout_Login.setSpacing(15)
        
        self.Label_User = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Label_User.setFont(font)
        self.Label_User.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_User.setText("Nombre de usuario");
        self.Layout_Login.addWidget(self.Label_User, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        #MESAJE DE INICIO DE SESION---------------------------------------------
        self.message_box = QMessageBox()
        self.message_box.setStyleSheet("""
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
        #-----------------------------------------------------------------------
        
        #INPUT DE NOMBRE DE USUARIO---------------------------------------------
        self.lineEdit_User = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_User.setFont(font)
        self.lineEdit_User.setStyleSheet("QWidget QLineEdit{\n"
"    border: 2px solid #00000080;\n"
"    border-radius: 5px;\n"
"    color: #ffffff;\n"
"    background-color: rgba(236, 240, 241, 0.5);\n"
"    }")
        self.lineEdit_User.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_User.setPlaceholderText("Usuario")
        self.Layout_Login.addWidget(self.lineEdit_User)
        #-----------------------------------------------------------------------
        
        self.Label_Pass = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Label_Pass.setFont(font)
        self.Label_Pass.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_Pass.setText("Contraseña");
        self.Layout_Login.addWidget(self.Label_Pass, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        #INPUT DE CONTRASEÑA----------------------------------------------------
        self.lineEdit_Pass = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_Pass.setFont(font)
        self.lineEdit_Pass.setStyleSheet("QWidget QLineEdit{\n"
"    border: 2px solid #00000080;\n"
"    border-radius: 5px;\n"
"    color: #ffffff;\n"
"    background-color: rgba(236, 240, 241, 0.5);\n"
"}")
        self.lineEdit_Pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_Pass.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_Pass.setPlaceholderText("Contraseña")
        self.Layout_Login.addWidget(self.lineEdit_Pass)
        #-----------------------------------------------------------------------
        
        #CHECKBOX PAREA MOSTRAR CONTRASEÑA--------------------------------------
        self.check_view_password = QCheckBox(self.verticalLayoutWidget)
        self.check_view_password.setFont(font);
        self.check_view_password.setText("Ver Contraseña")
        self.check_view_password.toggled.connect(self.showPass)
        self.Layout_Login.addWidget(self.check_view_password)
        #-----------------------------------------------------------------------
        
        #BOTON DE INICIAR SESION------------------------------------------------
        self.buttonGo = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setWeight(50)
        self.buttonGo.setFont(font)
        self.buttonGo.setStyleSheet("QPushButton{\n"
"    border-radius: 7px;\n"
"    border: 1px solid black;\n"
"    background: #ECF0F1; \n"
"    }\n"
"QPushButton:hover {\n"
"    background: #7F8C8D; \n"
"    color: #BDC3C7;\n"
"    }")
        self.buttonGo.setText("Iniciar")
        self.Layout_Login.addWidget(self.buttonGo)
        self.buttonGo.clicked.connect(self.logIn)
        #-----------------------------------------------------------------------
        
        MainWindow.setCentralWidget(self.LogIn_Window)
    
    def showPass(self, checked):
        if checked:
            self.lineEdit_Pass.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_Pass.setEchoMode(QtWidgets.QLineEdit.Password)
            
    #FUNCION PARA INICIO DE SESION----------------------------------------------
    def logIn(self):
        password = self.lineEdit_Pass.text()
        user_name = self.lineEdit_User.text()
        self.supabase: Client = create_client("https://qlsmhahdkovvqfauntde.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFsc21oYWhka292dnFmYXVudGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYwNjcxMjIsImV4cCI6MjA0MTY0MzEyMn0.K-LSXODTvSbvFqu6hnJWYiP8KDmm959LZB5xYQl6aPI")
    
        if password == "" or user_name == "":
            self.message_box.warning(self.message_box,"Error",
            "Algun campo vacio",
            self.message_box.StandardButton.Ok,
            self.message_box.StandardButton.Ok)
        elif password == "12345" and user_name == "Admin":
            self.main_window.close()
            self.goToHomeWindow()
        else:
            # Consulta a la base de datos para verificar las credenciales
            response = self.supabase.from_("empleados").select("*").eq("username", user_name).eq("password", password).execute()
            
            if response.data:
                # Si las credenciales son correctas
                user_data = response.data[0]  # Obtenemos los datos del usuario
                
                # Verificamos el puesto del usuario
                if user_data['puesto'] == "Administrador":
                    self.main_window.close()
                    self.goToHomeWindow()  # Ventana de administrador
                else:
                    self.main_window.close()
                    self.goToRegularHomeWindow()  # Ventana normal
            else:
                # Si las credenciales son incorrectas
                self.message_box.warning(self.message_box, "Error",
                                         "Credenciales incorrectas",
                                         self.message_box.StandardButton.Ok,
                                         self.message_box.StandardButton.Ok)

    #---------------------------------------------------------------------------
    
    #FUNCION PARA ABRIR LA VENTANA PRINCIPAL------------------------------------
    def goToHomeWindow(self):
        self.home_Window = HomeWindow()
        self.home_Window.show()
    #FUNCION PARA ABRIR LA VENTANA PRINCIPAL (usuarios no admin)------------------------------------
    def goToRegularHomeWindow(self):
        # Lógica para abrir la ventana de usuario regular
        pass   
    #---------------------------------------------------------------------------

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())