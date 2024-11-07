from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from Model.employee_model import EmpleadoModel

class EmpleadoController:
    def __init__(self, main_window):
        self.model = EmpleadoModel()
        self.view = main_window

        # Conectar señales
        self.view.addEmployee.clicked.connect(self.add_employee)
        self.view.updateEmployee.clicked.connect(self.update_employee)
        self.view.deleteEmployee.clicked.connect(self.delete_employee)
        self.view.employeeTable.currentCellChanged.connect(self.setDataOnWidgets)
    
    #NECESITA CAMBIOS
    def add_employee(self):
        cliente_data = {
            "nombre": self.view.customerName.text(),
            "apellido_paterno": self.view.customerLastPaternalName.text(),
            "apellido_materno": self.view.customerLastMaternalName.text(),
            "direccion": self.view.customerAddress.text(),
            "telefono": self.view.customerPhone.text(),
        }
        self.model.agregar_cliente(cliente_data)
        self.loadData()

    #CARGAR DATOS DE TODOS LAS TABLAS
    def loadData(self):
        empleados = self.model.obtener_empleados()
        self.view.buildingTable.setRowCount(0)  # Limpiar tabla antes de cargar datos
        obras = self.model.obtener_Obras()
        obraBox = [item['nombre'] for item in obras]
        self.view.employeeBuilding.addItems(obraBox)
        for row, data in enumerate(empleados):
            self.view.employeeTable.insertRow(row)
            rowData = list(data.values())

            for col, item in enumerate(rowData):
                if not isinstance(item, str):
                    item = str(item)
                self.view.employeeTable.setItem(row, col, QTableWidgetItem(item))

        self.view.employeeTable.setSortingEnabled(True)
        self.view.employeeTable.resizeColumnsToContents()

    #NECESITA CAMBIOS
    def update_employee(self):
        cliente_data = {
            "nombre": self.view.customerName.text(),
            "apellido_paterno": self.view.customerLastPaternalName.text(),
            "apellido_materno": self.view.customerLastMaternalName.text(),
            "direccion": self.view.customerAddress.text(),
            "telefono": self.view.customerPhone.text(),
        }
        self.model.actualizar_cliente(self.getIDFromTable(self.view.customerTable), cliente_data);
        self.loadData()
    #NECESITA CAMBIOS
    def delete_employee(self):
        self.model.eliminar_cliente(self.getIDFromTable(self.view.customerTable));
        self.loadData()
    #NECESITA CAMBIOS
    def setDataOnWidgets(self, row, col):
        if row == -1 or col == -1:
            # Limpia cada campo de entrada directamente
            self.view.customerName.setText("")
            self.view.customerLastPaternalName.setText("")
            self.view.customerLastMaternalName.setText("")
            self.view.customerAddress.setText("")
            self.view.customerPhone.setText("")
            return
        
        data = self.getDataFromTable(self.view.customerTable)
        
        self.view.customerName.setText(data[0])
        self.view.customerLastPaternalName.setText(data[1])
        self.view.customerLastMaternalName.setText(data[2])
        self.view.customerAddress.setText(data[3])
        self.view.customerPhone.setText(data[4])
        
    def getDataFromTable(self, table: QTableWidget):
        row = table.currentRow()
        data = []
    
        for col in range(table.columnCount()):
            if col == 0:  # Se evita agregar a la lista el elemento ID de la tabla
                continue
            item = table.item(row, col)
            data.append(item.text())
        return data

    
    def getIDFromTable(self, table: QTableWidget):
        row = table.currentRow()
        data = []
        for col in range(table.columnCount()):
            item = table.item(row, col).text()
            data.append(item)
        return data[0]