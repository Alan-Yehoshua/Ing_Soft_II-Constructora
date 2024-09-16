from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QPushButton
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from ui_mainwindow import Ui_MainWindow
from supabase import create_client, Client

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Inicializa la conexión a Supabase  BASE DE DATOS DE VICTOR
        self.supabase: Client = create_client("https://qlsmhahdkovvqfauntde.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFsc21oYWhka292dnFmYXVudGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYwNjcxMjIsImV4cCI6MjA0MTY0MzEyMn0.K-LSXODTvSbvFqu6hnJWYiP8KDmm959LZB5xYQl6aPI")
        self.loadData(self.ui.customerTable)
        
        # Se establece la columna "ID" de los empleados como oculta
        self.ui.employeeTable.setColumnHidden(0, True)
        
        # Configuración de los indices
        for val, btn in enumerate([self.ui.customerButton, self.ui.employeeButton, self.ui.supplierButton,
                                   self.ui.buildingButton, self.ui.materialButton, self.ui.dateButton, self.ui.requestButton]):
            btn.toggled.connect(lambda checked, btn=val: self.changeWindow(btn) if checked else None)
            
        self.ui.customerTable.currentCellChanged.connect(self.setDataOnWidgets)
        self.ui.employeeTable.currentCellChanged.connect(self.setDataOnWidgets)
        
        self.ui.addCustomer.clicked.connect(self.addData)
        self.ui.addEmployee.clicked.connect(self.addData)
        
        self.ui.updateCustomer.clicked.connect(self.modifyData)
        self.ui.updateEmployee.clicked.connect(self.modifyData)
        
        self.ui.deleteCustomer.clicked.connect(self.deleteData)
        self.ui.deleteEmployee.clicked.connect(self.deleteData)
        
    def changeWindow(self, index: int):
        self.ui.stackedWidget.setCurrentIndex(index)
        
        indexDict = {
            0: self.ui.customerTable,
            1: self.ui.employeeTable
        }
        
        # Bloqueo tempral debido a la cantidad de paginas en self.ui.stackedWidget
        if index > 1:
            index = 1
        
        # Carga los datos a la tabla a trabajar
        self.loadData(indexDict[index])
        
        # Limpia la seleccion de las demás tablas
        for idx, table in enumerate([self.ui.customerTable, self.ui.employeeTable]):
            if idx == index: # Si los indices coinciden, se salta la iteración
                continue
            
            table.setSortingEnabled(False)
            table.clearSelection()
                
    def loadData(self, table: QTableWidget):
        # Diccionario que almacena la tabla a consultar con supabase
        # Se compara la tabla de la interfaz para elegir la tabla de Supabase
        sqlTable = {
            self.ui.customerTable: "cliente",
            self.ui.employeeTable: "empleados"
        }
        
        response = self.supabase.table(sqlTable[table]).select("*").execute()
        
        # Limpiar la tabla antes de cargar datos
        table.setRowCount(0)
        
        for row, data in enumerate(response.data):
            table.insertRow(row)
            rowData = list(data.values()) # Convierte los datos en una lista
                
            for col, item in enumerate(rowData):
                if not isinstance(item, str):
                    item = str(item)
                    
                self.setCellItem(table, row, col, QTableWidgetItem(item))
        
        table.setSortingEnabled(True)
        table.resizeColumnsToContents() # Ajusta el tamaño de las columnas al ancho de los datos
        
    def setDataOnWidgets(self, row, col):
        sender = self.sender()
        # Si el elemento en la interfaz que llamo a la función no fue un QTableWidget, termina la función
        if isinstance(sender, QTableWidget): 
            table = sender
        else:
            return
        
        # Diccionario que almacena una lista con los objetos a rellenar en base al orden de las columnas en la tabla
        widgetsDict = {
            self.ui.customerTable: [self.ui.customerName, self.ui.customerLastPaternalName, self.ui.customerLastMaternalName, self.ui.customerAddress, self.ui.customerPhone],
            self.ui.employeeTable: [self.ui.employeeName, self.ui.employeePaternalLastName, self.ui.employeeMaternalLastName, self.ui.employeeMail,
                                    self.ui.employeePosition, self.ui.employeeUsername, self.ui.employeePassword, self.ui.employeeBuilding]
        }
        widgetList = widgetsDict[table]
        
        # Si la seleccion es nula, entonces limpia los widgets y retorna
        if row == -1 or col == -1:
            for widget in widgetList:
                if isinstance(widget, QLineEdit):
                    widget.setText("")
                elif isinstance(widget, QComboBox):
                    widget.setCurrentIndex(0)
                    
            return
        
        # Recupera los datos de la fila seleccionada
        data = self.getDataFromTable(table)
        
        # Itera en los widgets para insertar los datos recuperados
        for idx, widget in enumerate(widgetList):
            if isinstance(widget, QLineEdit):
                widget.setText(data[idx])
            elif isinstance(widget, QComboBox) and table == self.ui.employeeTable:
                widget.setCurrentIndex(0 if data[idx] == "Trabajador" else 1)
        
    def getDataFromTable(self, table: QTableWidget):
        row = table.currentRow()
        data = []
        
        for col in range(table.columnCount()):
            if col == 0: # Se evita agregar a la lista el elemento ID de la tabla
                continue 
            
            item = table.item(row, col).text()
            data.append(item)
            
        return data
    
    def addData(self):
        sender = self.sender()
        if isinstance(sender, QPushButton):
            button = sender
        else:
            return
        
        tableDict = {
            self.ui.addCustomer: self.ui.customerTable,
            self.ui.addEmployee: self.ui.employeeTable
        }
        
        sqlTable = {
            self.ui.addCustomer: "cliente",
            self.ui.addEmployee: "empleados"
        }
        
        table = tableDict[button]
        index = self.getNextIndex(table)
        jsonDict = {
            self.ui.addCustomer: {"id_cliente": index,
                                  "nombre": self.ui.customerName.text(),
                                  "apellido_paterno": self.ui.customerLastPaternalName.text(),
                                  "apellido_materno": self.ui.customerLastMaternalName.text(),
                                  "direccion": self.ui.customerAddress.text(),
                                  "telefono": self.ui.customerPhone.text()},
            self.ui.addEmployee: {"id_empleados": index,
                                  "nombre": self.ui.employeeName.text(),
                                  "apellido_paterno": self.ui.employeePaternalLastName.text(),
                                  "apellido_materno": self.ui.employeeMaternalLastName.text(),
                                  "email": self.ui.employeeMail.text(),
                                  "puesto": self.ui.employeePosition.currentText(),
                                  "username": self.ui.employeeUsername.text(),
                                  "password": self.ui.employeePassword.text(),
                                  "id_obra": self.ui.employeeBuilding.text()}
        }
        
        rowFormat = {
            self.ui.addCustomer: [str(index), self.ui.customerName.text(), self.ui.customerLastPaternalName.text(), self.ui.customerLastMaternalName.text(), 
                                  self.ui.customerAddress.text(), self.ui.customerPhone.text()],
            self.ui.addEmployee: [str(index), self.ui.employeeName.text(), self.ui.employeePaternalLastName.text(), self.ui.employeeMaternalLastName.text(),
                                  self.ui.employeeMail.text(), self.ui.employeePosition.currentText(), self.ui.employeeUsername.text(),
                                  self.ui.employeePassword.text(), self.ui.employeeBuilding.text()]
        }
        
        self.supabase.table(sqlTable[button]).insert(jsonDict[button]).execute()
        
        row = table.rowCount()
        table.insertRow(row)
        
        for col, item in enumerate(rowFormat[button]):
            self.setCellItem(table, row, col, QTableWidgetItem(item))
        table.resizeColumnsToContents()
    
    def modifyData(self):
        sender = self.sender()
        if isinstance(sender, QPushButton):
            button = sender
        else:
            return
        
        tableDict = {
            self.ui.updateCustomer: self.ui.customerTable,
            self.ui.updateEmployee: self.ui.employeeTable
        }
        
        sqlTable = {
            self.ui.updateCustomer: "cliente",
            self.ui.updateEmployee: "empleados"
        }
        
        indexColumn = {
            self.ui.updateCustomer: "id_cliente",
            self.ui.updateEmployee: "id_empleados"
        }
        
        jsonDict = {
            self.ui.updateCustomer: {"nombre": self.ui.customerName.text(),
                                     "apellido_paterno": self.ui.customerLastPaternalName.text(),
                                     "apellido_materno": self.ui.customerLastMaternalName.text(),
                                     "direccion": self.ui.customerAddress.text(),
                                     "telefono": self.ui.customerPhone.text()},
            self.ui.updateEmployee: {"nombre": self.ui.employeeName.text(),
                                     "apellido_paterno": self.ui.employeePaternalLastName.text(),
                                     "apellido_materno": self.ui.employeeMaternalLastName.text(),
                                     "email": self.ui.employeeMail.text(),
                                     "puesto": self.ui.employeePosition.currentText(),
                                     "username": self.ui.employeeUsername.text(),
                                     "password": self.ui.employeePassword.text(),
                                     "id_obra": self.ui.employeeBuilding.text()}
        }
        
        table = tableDict[button]
        row = table.currentRow()
        index = int(table.item(row, 0).text())
        
        rowFormat = {
            self.ui.updateCustomer: [str(index), self.ui.customerName.text(), self.ui.customerLastPaternalName.text(), self.ui.customerLastMaternalName.text(), 
                                     self.ui.customerAddress.text(), self.ui.customerPhone.text()],
            self.ui.updateEmployee: [str(index), self.ui.employeeName.text(), self.ui.employeePaternalLastName.text(), self.ui.employeeMaternalLastName.text(),
                                     self.ui.employeeMail.text(), self.ui.employeePosition.currentText(), self.ui.employeeUsername.text(),
                                     self.ui.employeePassword.text(), self.ui.employeeBuilding.text()]
        }
        
        self.supabase.table(sqlTable[button]).update(jsonDict[button]).eq(indexColumn[button], index).execute()
        
        for col, item in enumerate(rowFormat[button]):
            self.setCellItem(table, row, col, QTableWidgetItem(item))
        table.resizeColumnsToContents()
    
    def deleteData(self):
        sender = self.sender()
        if isinstance(sender, QPushButton):
            button = sender
        else:
            return
        
        tableDict = {
            self.ui.deleteCustomer: self.ui.customerTable,
            self.ui.deleteEmployee: self.ui.employeeTable
        }
        
        sqlTable = {
            self.ui.deleteCustomer: "cliente",
            self.ui.deleteEmployee: "empleados"
        }
        
        indexColumn = {
            self.ui.deleteCustomer: "id_cliente",
            self.ui.deleteEmployee: "id_empleados"
        }
        
        table = tableDict[button]
        row = table.currentRow()
        index = int(table.item(row, 0).text())
        
        self.supabase.table(sqlTable[button]).delete().eq(indexColumn[button], index).execute()
        table.removeRow(row)
    
    def getNextIndex(self, table: QTableWidget):
        sqlTable = {
            self.ui.customerTable: "cliente",
            self.ui.employeeTable: "empleados"
        }
        
        indexColumn = {
            self.ui.customerTable: "id_cliente",
            self.ui.employeeTable: "id_empleados"
        }
        
        # Esto es igual a "SELECT {indexColumn[table]} FROM {sqlTabe[table]} ORDER BY {indexColumn[table]} DESC LIMIT 1;"
        response = self.supabase.table(sqlTable[table]).select(indexColumn[table]).order(indexColumn[table], desc=True).limit(1).execute()

        # Verifica si hay datos en la respuesta
        data = response.data
        if data:
            maxID = data[0][indexColumn[table]]
            return maxID + 1
        else:
            # Si no hay datos, significa que la tabla está vacía
            return 1

        
    # Regalito personal de Néstor, inserta los datos a cualquier tabla con el formato que se decida
    def setCellItem(self, table: QTableWidget, row: int, col: int, item: QTableWidgetItem, foreground: QColor=QColor("#fff"), alignment: Qt.AlignmentFlag=Qt.AlignmentFlag.AlignVCenter|Qt.AlignmentFlag.AlignLeft, font: QFont=QFont("Segoe UI", 10)):
        item.setTextAlignment(alignment) # Establece la alineación del texto
        item.setForeground(foreground) # Establece el color de la fuente
        item.setFont(font) # Establece la fuente del texto
        
        # Establece el elemento en la celda específica de la tabla
        table.setItem(row, col, item)