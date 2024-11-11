from Model.auth_model import AuthModel
from View.login_window import LogInWindow
from View.main_window import MainWindow
from View.main_window_e import MainWindowE

class AuthController:
    def __init__(self, login_window: LogInWindow):
        self.model = AuthModel()
        self.view = login_window

    def log_in(self):
        user_name = self.view.username.text()
        password = self.view.password.text()
        
        if not user_name or not password:
            self.view.show_message("Error", "Algun campo vacio")
            return

        #Verificar las credenciales
        user_data = self.model.verify_credentials(user_name, password)
        if user_data:
            user_data = user_data[0]  # Obtenemos el primer resultado
            if self.model.is_admin(user_data):
                self.view.close()
                self.go_to_home_window()
            else:
                self.view.close()
                self.go_to_regular_home_window()
        else:
           self.view.show_message("Error", "Credenciales incorrectas")

    def go_to_home_window(self):
        self.home_window = MainWindow()  # Ventana de administrador
        self.home_window.show()

    def go_to_regular_home_window(self):
        self.home_window_e = MainWindowE()  # Ventana de administrador
        self.home_window_e.show()
        pass