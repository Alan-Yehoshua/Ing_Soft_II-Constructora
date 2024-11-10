import sys
from PyQt5.QtWidgets import QApplication
from View.login_window import LogInWindow
from Controller.auth_controller import AuthController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Crear instancias
    login_window = LogInWindow()
    # Crear controlador de autenticación
    auth_controller = AuthController(login_window)
    # Establecer conexiones
    login_window.controller = auth_controller
    # Mostrar ventana de login
    login_window.show()
    sys.exit(app.exec_())