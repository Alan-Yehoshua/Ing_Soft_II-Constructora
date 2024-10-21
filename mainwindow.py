from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QPushButton
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from supabase import create_client, Client

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("HomePage.ui", self)
        
        # Inicializa la conexión a Supabase  BASE DE DATOS DE VICTOR
        self.supabase: Client = create_client("https://qlsmhahdkovvqfauntde.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFsc21oYWhka292dnFmYXVudGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYwNjcxMjIsImV4cCI6MjA0MTY0MzEyMn0.K-LSXODTvSbvFqu6hnJWYiP8KDmm959LZB5xYQl6aPI")
        self.loadData(self.customerTable)
        self.loadData(self.employeeTable)
        self.loadData(self.buildingTable)
        self.loadData(self.suplierTable)
        self.loadData(self.materialTable)
        
        # Se establece la columna "ID" de los empleados como oculta
        self.employeeTable.setColumnHidden(0, True)
        self.customerTable.setColumnHidden(0, True)
        self.buildingTable.setColumnHidden(0, True)
        self.suplierTable.setColumnHidden(0,True)
        self.materialTable.setColumnHidden(0,True)
        
        # Configuración de los indices
        for val, btn in enumerate([self.customerButton, self.employeeButton, self.supplierButton,
                                   self.buildingButton, self.materialButton, self.dateButton, self.requestButton]):
            btn.toggled.connect(lambda checked, btn=val: self.changeWindow(btn) if checked else None)
            
        self.customerTable.currentCellChanged.connect(self.setDataOnWidgets)
        self.employeeTable.currentCellChanged.connect(self.setDataOnWidgets)
        self.buildingTable.currentCellChanged.connect(self.setDataOnWidgets)
        self.suplierTable.currentCellChanged.connect(self.setDataOnWidgets)
        self.materialTable.currentCellChanged.connect(self.setDataOnWidgets)

        self.addCustomer.clicked.connect(self.addData)
        self.addEmployee.clicked.connect(self.addData)
        self.addSuplier.clicked.connect(self.addData)
        self.addMaterial.clicked.connect(self.addData)
        self.addBuilding.clicked.connect(self.addData)

        self.updateCustomer.clicked.connect(self.modifyData)
        self.updateEmployee.clicked.connect(self.modifyData)
        self.updateSuplier.clicked.connect(self.modifyData)
        self.updateMaterial.clicked.connect(self.modifyData)
        self.updateBuilding.clicked.connect(self.modifyData)

        self.deleteCustomer.clicked.connect(self.deleteData)
        self.deleteEmployee.clicked.connect(self.deleteData)
        self.deleteSuplier.clicked.connect(self.deleteData)
        self.deleteMaterial.clicked.connect(self.deleteData)
        self.deleteBuilding.clicked.connect(self.deleteData)

        
    def changeWindow(self, index: int):
        self.stackedWidget.setCurrentIndex(index)
        
        indexDict = {
            0: self.customerTable,
            1: self.employeeTable,
            2: self.suplierTable,
            3: self.materialTable,
            4: self.buildingTable
        }
        
        # Limpia los widgets cuando se cambia de pestaña
        widgetsDict = {
            0: [self.customerName, self.customerLastPaternalName, self.customerLastMaternalName, self.customerAddress, self.customerPhone],
            1: [self.employeeName, self.employeePaternalLastName, self.employeeMaternalLastName, self.employeeMail,
                self.employeePosition, self.employeeUsername, self.employeePassword, self.employeeBuilding],
            2: [self.suplierName, self.suplierNumber],
            3: [self.materialName, self.materialCant, self.materialProv],
            4: [self.buildingProyect, self.buildingAddress, self.buildindgDate, self.buildingCustomer]
        }
        
        widgetList = widgetsDict.get(index, [])
        for widget in widgetList:
            if isinstance(widget, QLineEdit):
                widget.setText("")
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
        
        # Carga los datos a la tabla correspondiente
        self.loadData(indexDict[index])
        
        # Limpia la selección de las demás tablas
        for idx, table in enumerate([self.customerTable, self.employeeTable, self.suplierTable, self.materialTable, self.buildingTable]):
            if idx == index:  # Si los índices coinciden, se salta la iteración
                continue
            table.setSortingEnabled(False)
            table.clearSelection()

                
    def loadData(self, table: QTableWidget):
        # Diccionario que almacena la tabla a consultar con supabase
        # Se compara la tabla de la interfaz para elegir la tabla de Supabase
        sqlTable = {
            self.customerTable: "cliente",
            self.employeeTable: "empleados",
            self.buildingTable: "obra",
            self.suplierTable: "proveedor",   # Nueva tabla para Supplier
            self.materialTable: "material"   # Nueva tabla para Material
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
            self.customerTable: [self.customerName, self.customerLastPaternalName, self.customerLastMaternalName, self.customerAddress, self.customerPhone],
            self.employeeTable: [self.employeeName, self.employeePaternalLastName, self.employeeMaternalLastName, self.employeeMail,
                                    self.employeePosition, self.employeeUsername, self.employeePassword, self.employeeBuilding],
            self.suplierTable: [self.suplierName, self.suplierNumber],
            self.materialTable: [self.materialName, self.materialCant, self.materialProv],
            self.buildingTable: [self.buildingProyect, self.buildingAddress, self.buildindgDate, self.buildingCustomer]
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
            elif isinstance(widget, QComboBox) and table == self.employeeTable:
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
        
        # Diccionarios de referencia
        tableDict = {
            self.addCustomer: self.customerTable,
            self.addEmployee: self.employeeTable,
            self.addSuplier: self.suplierTable,
            self.addMaterial: self.materialTable,
            self.addBuilding: self.buildingTable,
        }

        sqlTable = {
            self.addCustomer: "cliente",
            self.addEmployee: "empleados",
            self.addSuplier: "proveedor",
            self.addMaterial: "material",
            self.addBuilding: "obra",
        }


        
        table = tableDict[button]
        index = self.getNextIndex(table)
        jsonDict = {
            self.addCustomer: {
                "id_cliente": index,
                "nombre": self.customerName.text(),
                "apellido_paterno": self.customerLastPaternalName.text(),
                "apellido_materno": self.customerLastMaternalName.text(),
                "direccion": self.customerAddress.text(),
                "telefono": self.customerPhone.text(),
            },
            self.addEmployee: {
                "id_empleados": index,
                "nombre": self.employeeName.text(),
                "apellido_paterno": self.employeePaternalLastName.text(),
                "apellido_materno": self.employeeMaternalLastName.text(),
                "email": self.employeeMail.text(),
                "puesto": self.employeePosition.currentText(),
                "username": self.employeeUsername.text(),
                "password": self.employeePassword.text(),
                "id_obra": self.employeeBuilding.text(),
            },
            self.addSuplier: {
                "id_proveedor": index,
                "nombre": self.suplierName.text(),
                "telefono": self.suplierNumber.text(),
            },
            self.addMaterial: {
                "id_material": index,
                "nombre": self.materialName.text(),
                "cantidad": self.materialCant.text(),
                "id_proveedor": self.materialProv.text(),
            },
            self.addBuilding: {
                "id_obra": index,
                "nombre": self.buildingProyect.text(),
                "ubicacion": self.buildingAddress.text(),
                "fecha_inicio": self.buildindgDate.text(),
                "id_cliente": self.buildingCustomer.text(),
            }
        }
        #poner validacion de provedor id en obra
                
            

        
        rowFormat = {
            self.addCustomer: [str(index), self.customerName.text(), self.customerLastPaternalName.text(), self.customerLastMaternalName.text(), 
                                  self.customerAddress.text(), self.customerPhone.text()],
            self.addEmployee: [str(index), self.employeeName.text(), self.employeePaternalLastName.text(), self.employeeMaternalLastName.text(),
                                  self.employeeMail.text(), self.employeePosition.currentText(), self.employeeUsername.text(),
                                  self.employeePassword.text(), self.employeeBuilding.text()],
            self.addSuplier: [str(index), self.suplierName.text(), self.suplierNumber.text()],
            self.addMaterial: [str(index), self.materialName.text(), self.materialCant.text(), self.materialProv.text(), ],
            self.addBuilding: [str(index),  self.buildingProyect.text(), self.buildingAddress.text(), self.buildindgDate.text(), self.buildingCustomer.text()],
       
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

        # Diccionarios de referencia
        tableDict = {
            self.updateCustomer: self.customerTable,
            self.updateEmployee: self.employeeTable,
            self.updateSuplier: self.suplierTable,
            self.updateMaterial: self.materialTable,
            self.updateBuilding: self.buildingTable,
        }

        sqlTable = {
            self.updateCustomer: "cliente",
            self.updateEmployee: "empleados",
            self.updateSuplier: "proveedor",
            self.updateMaterial: "material",
            self.updateBuilding: "obra",
        }

        indexColumn = {
            self.updateCustomer: "id_cliente",
            self.updateEmployee: "id_empleados",
            self.updateSuplier: "id_proveedor",
            self.updateMaterial: "id_material",
            self.updateBuilding: "id_obra",
        }

        # Obtener la tabla correspondiente
        table = tableDict[button]
        
        # Obtener el índice de la fila seleccionada
        selected_row = table.currentRow()
        if selected_row == -1:
            return  # No hay ninguna fila seleccionada

        # Obtener el valor del ID desde la primera columna de la fila seleccionada (columna 0, que está oculta)
        index = table.item(selected_row, 0).text()

        # Diccionario JSON con los datos a actualizar
        jsonDict = {
            self.updateCustomer: {
                "id_cliente": index,
                "nombre": self.customerName.text(),
                "apellido_paterno": self.customerLastPaternalName.text(),
                "apellido_materno": self.customerLastMaternalName.text(),
                "direccion": self.customerAddress.text(),
                "telefono": self.customerPhone.text(),
            },
            self.updateEmployee: {
                "id_empleados": index,
                "nombre": self.employeeName.text(),
                "apellido_paterno": self.employeePaternalLastName.text(),
                "apellido_materno": self.employeeMaternalLastName.text(),
                "email": self.employeeMail.text(),
                "puesto": self.employeePosition.currentText(),
                "username": self.employeeUsername.text(),
                "password": self.employeePassword.text(),
                "id_obra": self.employeeBuilding.text(),
            },
            self.updateSuplier: {
                "id_proveedor": index,
                "nombre": self.suplierName.text(),
                "telefono": self.suplierNumber.text(),
            },
            self.updateMaterial: {
                "id_material": index,
                "nombre": self.materialName.text(),
                "cantidad": self.materialCant.text(),
                "id_proveedor": self.materialProv.text(),
            },
            self.updateBuilding: {
                "id_obra": index,
                "nombre": self.buildingProyect.text(),
                "ubicacion": self.buildingAddress.text(),
                "fecha_inicio": self.buildindgDate.text(),
                "id_cliente": self.buildingCustomer.text(),
            }
        }

        # Realizar la actualización en la base de datos
        self.supabase.table(sqlTable[button]).update(jsonDict[button]).eq(indexColumn[button], index).execute()
        


        # Actualizar la tabla con los nuevos datos
        for col, item in enumerate(jsonDict[button].values()):
            self.setCellItem(table, selected_row, col, QTableWidgetItem(str(item)))

        table.resizeColumnsToContents()

    
    def deleteData(self):
        sender = self.sender()
        if isinstance(sender, QPushButton):
            button = sender
        else:
            return
        
        tableDict = {
            self.deleteCustomer: self.customerTable,
            self.deleteEmployee: self.employeeTable,
            self.deleteSuplier: self.suplierTable,
            self.deleteMaterial: self.materialTable,
            self.deleteBuilding: self.buildingTable,

        }

        sqlTable = {
            self.deleteCustomer: "cliente",
            self.deleteEmployee: "empleados",
            self.deleteSuplier: "proveedor",
            self.deleteMaterial: "material",
            self.deleteBuilding: "obra",
        }

        indexColumn = {
            self.deleteCustomer: "id_cliente",
            self.deleteEmployee: "id_empleados",
            self.deleteSuplier: "id_proveedor",
            self.deleteMaterial: "id_material",
            self.deleteBuilding: "id_obra",
        }
        
        table = tableDict[button]
        row = table.currentRow()
        index = int(table.item(row, 0).text())
        
        self.supabase.table(sqlTable[button]).delete().eq(indexColumn[button], index).execute()
        table.removeRow(row)
    
    def getNextIndex(self, table: QTableWidget):
        sqlTable = {
            self.customerTable: "cliente",
            self.employeeTable: "empleados",
            self.buildingTable: "obra",
            self.suplierTable: "proveedor",   
            self.materialTable: "material"   
        }


        indexColumn = {
            self.customerTable: "id_cliente",
            self.employeeTable: "id_empleados",
            self.buildingTable: "id_obra",
            self.suplierTable: "id_proveedor", 
            self.materialTable: "id_material"
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