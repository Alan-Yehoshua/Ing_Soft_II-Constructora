from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.uic import loadUi
import sys
from supabase import create_client, Client

#BASE DE DATOS DE ALAN
url = "https://njgqpwaocrkghoaetovp.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5qZ3Fwd2FvY3JrZ2hvYWV0b3ZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU1ODY0MDYsImV4cCI6MjA0MTE2MjQwNn0.t-WxD9PtP-oZBvxMGiWmuENSPU_e9nD81B9ima1dOlU"

class HomeWindow(QMainWindow):
    def __init__(self):
        super(HomeWindow, self).__init__()
        loadUi("HomePage.ui", self)

        self.CustomerButton.clicked.connect(self.customerPage)
        self.EmployeButton.clicked.connect(self.employePage)
        # Inicializa la conexión a Supabase  BASE DE DATOS DE VICTOR
        self.supabase: Client = create_client("https://qlsmhahdkovvqfauntde.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFsc21oYWhka292dnFmYXVudGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYwNjcxMjIsImV4cCI6MjA0MTY0MzEyMn0.K-LSXODTvSbvFqu6hnJWYiP8KDmm959LZB5xYQl6aPI")
        self.loadCustomerData()
        
        self.TableCustomer.currentCellChanged.connect(self.transferir_datos_a_inputs)
        self.TableEmploye.currentCellChanged.connect(self.transferir_datos_empleado)

    def transferir_datos_a_inputs(self, fila, columna):
        # Obtener los datos de la fila seleccionada y transferirlos a los QLineEdit
        self.NameCustomer.setText(self.TableCustomer.item(fila, 1).text())
        self.LastNamePaCustomer.setText(self.TableCustomer.item(fila, 2).text())
        self.AddressCustomer.setText(self.TableCustomer.item(fila, 3).text())
        self.NumberCustomer.setText(self.TableCustomer.item(fila, 4).text())
        
        # Función para transferir datos de empleados seleccionados a QLineEdit
    def transferir_datos_empleado(self, fila, columna):
        self.NameEmploye.setText(self.TableEmploye.item(fila, 0).text())
        self.LastNamePaEmploye.setText(self.TableEmploye.item(fila, 1).text())
        self.LastNamePaEmploye_2.setText(self.TableEmploye.item(fila, 2).text())
        self.EmailEmploye.setText(self.TableEmploye.item(fila, 3).text())
        self.PositionEmploye.setCurrentIndex(0 if self.TableEmploye.item(fila, 4).text() == "Trabajador" else 1)
        self.UserEmploye.setText(self.TableEmploye.item(fila, 5).text())
        self.PasswordEmploye.setText(self.TableEmploye.item(fila, 6).text())

    def customerPage(self):
        self.stackedWidget.setCurrentIndex(0)
        self.loadCustomerData()

    def employePage(self):
        self.stackedWidget.setCurrentIndex(1)
        self.loadEmployeData()

    def loadCustomerData(self):
        # Obtiene los datos de la tabla de clientes
        response = self.supabase.table("cliente").select("*").execute()

        # Asumiendo que tienes una QTableWidget llamada customerTable
        self.TableCustomer.setRowCount(0)
        for row, data in enumerate(response.data):
            self.TableCustomer.insertRow(row)
            for col, (key, value) in enumerate(data.items()):
                self.TableCustomer.setItem(row, col, QTableWidgetItem(str(value)))

    # Función para cargar datos de empleados en la tabla de empleados
    def loadEmployeData(self):
        # Consulta a la tabla "empleados" en Supabase
        response = self.supabase.table("empleados").select("*").execute()

        # Limpiar la tabla antes de cargar datos
        self.TableEmploye.setRowCount(0)
        
        # Insertar datos en la tabla de empleados
        for row, data in enumerate(response.data):
            self.TableEmploye.insertRow(row)
            self.TableEmploye.setItem(row, 0, QTableWidgetItem(data['nombre']))
            self.TableEmploye.setItem(row, 1, QTableWidgetItem(data['apellido_paterno']))
            self.TableEmploye.setItem(row, 2, QTableWidgetItem(data['apellido_materno']))
            self.TableEmploye.setItem(row, 3, QTableWidgetItem(data['email']))
            self.TableEmploye.setItem(row, 4, QTableWidgetItem(data['puesto']))
            self.TableEmploye.setItem(row, 5, QTableWidgetItem(data['username']))
            self.TableEmploye.setItem(row, 6, QTableWidgetItem(data['password']))  # Mostrar la contraseña
            self.TableEmploye.setItem(row, 7, QTableWidgetItem(str(data['id_obra'])))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = HomeWindow()
    ui.show()
    sys.exit(app.exec_())

