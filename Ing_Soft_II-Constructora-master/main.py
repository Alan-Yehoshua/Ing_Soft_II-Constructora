from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.uic import loadUi
import sys
from supabase import create_client, Client


class HomeWindow(QMainWindow):
    def __init__(self):
        super(HomeWindow, self).__init__()
        loadUi("HomePage.ui", self)

        self.CustomerButton.clicked.connect(self.customerPage)
        self.EmployeButton.clicked.connect(self.employePage)

        # Inicializa la conexión a Supabase
        self.supabase: Client = create_client("https://qlsmhahdkovvqfauntde.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFsc21oYWhka292dnFmYXVudGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYwNjcxMjIsImV4cCI6MjA0MTY0MzEyMn0.K-LSXODTvSbvFqu6hnJWYiP8KDmm959LZB5xYQl6aPI")

    def customerPage(self):
        self.stackedWidget.setCurrentIndex(0)
        self.loadCustomerData()

    def employePage(self):
        self.stackedWidget.setCurrentIndex(1)

    def loadCustomerData(self):
        # Obtiene los datos de la tabla de clientes
        response = self.supabase.table("cliente").select("*").execute()

        # Asumiendo que tienes una QTableWidget llamada customerTable
        self.TableCustomer.setRowCount(0)
        for row, data in enumerate(response.data):
            self.TableCustomer.insertRow(row)
            for col, (key, value) in enumerate(data.items()):
                self.TableCustomer.setItem(row, col, QTableWidgetItem(str(value)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = HomeWindow()
    ui.show()
    sys.exit(app.exec_())