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
        self.BuildingButton.clicked.connect(self.buildingPage)

        #CONEXION A LA BASE DE DATOS Y CARGA DE DATOS---------------------------
        self.supabase: Client = create_client("https://hgpzmxwqwscqoaaqplrj.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhncHpteHdxd3NjcW9hYXFwbHJqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY0NTE4MjUsImV4cCI6MjA0MjAyNzgyNX0.C7bldU67QGAUlQTcOCMbL-MDu-IOthH-0RlUN8LATaA")
        self.LoadData('cliente', self.TableCustomer) #(NOMBRE DE LA TABLA EN DB, QTableWidget donde se pondran los datos)
        self.LoadData('empleado', self.TableEmploye)
        self.LoadData('obra', self.TableBuilding)
        #-----------------------------------------------------------------------
        
        self.TableCustomer.cellClicked.connect(self.cellsToInputsCustomer)
        
    #FUNCIONES PARA MOVERNOS ENTRE PAGINAS--------------------------------------
    def customerPage(self):
        self.stackedWidget.setCurrentIndex(0)

    def employePage(self):
        self.stackedWidget.setCurrentIndex(1)
        
    def buildingPage(self):
        self.stackedWidget.setCurrentIndex(2)

    #---------------------------------------------------------------------------
    
    #FUNCION PARA MANDAR DATOS DE LAS FILAS A LOS INPUTS (SOLO PARA CLIENTES TEMP)
    def cellsToInputsCustomer(self, fila, columna):
        self.NameCustomer.setText(self.TableCustomer.item(fila, 1).text())
        self.LastNamePaCustomer.setText(self.TableCustomer.item(fila, 2).text())
        self.AddressCustomer.setText(self.TableCustomer.item(fila, 3).text())
        self.NumberCustomer.setText(self.TableCustomer.item(fila, 4).text())
    #---------------------------------------------------------------------------
    
    #FUNCION PARA CARGAR LOS DATOS
    def LoadData(self, tableNameDB, tableName):
        # Obtiene los datos de la tabla de clientes
        response = self.supabase.table(tableNameDB).select("*").execute()
        # Asumiendo que tienes una QTableWidget llamada customerTable
        tableName.setRowCount(0)
        for row, data in enumerate(response.data):
            tableName.insertRow(row)
            for col, (key, value) in enumerate(data.items()):
                tableName.setItem(row, col, QTableWidgetItem(str(value)))
    #---------------------------------------------------------------------------


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = HomeWindow()
    ui.show()
    sys.exit(app.exec_())