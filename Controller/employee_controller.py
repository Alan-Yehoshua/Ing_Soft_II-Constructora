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
    
    #TEST
    def add_employee(self):
        employee_data = {
            "nombre": self.view.employeeName.text(),
            "apellido_paterno": self.view.employeePaternalLastName.text(),
            "apellido_materno": self.view.employeeMaternalLastName.text(),
            "email": self.view.employeeMail.text(),
            "puesto": self.view.employeePosition.currentText(),
            "username": self.view.employeeUsername.text(),
            "password": self.view.employeePassword.text(),
            "id_obra": self.model.obtener_id_obra(self.view.employeeBuilding.currentText())
        }
        self.model.agregar_empleados(employee_data)
        self.loadData()

    #CARGAR DATOS DE TODOS LAS TABLAS
    def loadData(self):
        empleados = self.model.obtener_empleados()
        self.view.employeeTable.setRowCount(0)  # Limpiar tabla antes de cargar datos
        obras = self.model.obtener_Obras()
        obraBox = [item['nombre'] for item in obras]
        self.view.employeeBuilding.clear()
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
        employee_data = {
            "nombre": self.view.employeeName.text(),
            "apellido_paterno": self.view.employeePaternalLastName.text(),
            "apellido_materno": self.view.employeeMaternalLastName.text(),
            "email": self.view.employeeMail.text(),
            "puesto": self.view.employeePosition.currentText(),
            "username": self.view.employeeUsername.text(),
            "password": self.view.employeePassword.text(),
            "id_obra": self.model.obtener_id_obra(self.view.employeeBuilding.currentText())
        }
        self.model.actualizar_empleados(self.getIDFromTable(self.view.employeeTable), employee_data);
        self.loadData()
        
    #NECESITA CAMBIOS
    def delete_employee(self):
        self.model.eliminar_empleados(self.getIDFromTable(self.view.employeeTable));
        self.loadData()
        
    #NECESITA CAMBIOS
    def setDataOnWidgets(self, row, col):
        if row == -1 or col == -1:
            # Limpia cada campo de entrada directamente
            self.view.employeeName.setText("")
            self.view.employeePaternalLastName.setText("")
            self.view.employeeMaternalLastName.setText("")
            self.view.employeePosition.setCurrentIndex(0)
            self.view.employeeMail.setText("")
            self.view.employeeUsername.setText("")
            self.view.employeePassword.setText("")
            self.view.employeeBuilding.setCurrentIndex(0)
            return
        
        data = self.getDataFromTable(self.view.employeeTable)
        
        self.view.employeeName.setText(data[0])
        self.view.employeePaternalLastName.setText(data[1])
        self.view.employeeMaternalLastName.setText(data[2])
        self.view.employeeMail.setText(data[3])
        indexP = self.view.employeePosition.findText(data[4])  
        self.view.employeePosition.setCurrentIndex(indexP)
        self.view.employeeUsername.setText(data[5])
        self.view.employeePassword.setText(data[6])
        indexB = self.view.employeeBuilding.findText(data[7])
        self.view.employeeBuilding.setCurrentIndex(indexB)
        
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