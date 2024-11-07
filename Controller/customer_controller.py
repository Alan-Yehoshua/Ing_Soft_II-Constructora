from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from Model.customer_model import ClienteModel

class ClienteController:
    def __init__(self, main_window):
        self.model = ClienteModel()
        self.view = main_window

        # Conectar señales
        self.view.addCustomer.clicked.connect(self.add_customer)
        self.view.updateCustomer.clicked.connect(self.update_customer)
        self.view.deleteCustomer.clicked.connect(self.delete_customer)
        self.view.customerTable.currentCellChanged.connect(self.setDataOnWidgets)
        
    def add_customer(self):
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
        clientes = self.model.obtener_clientes()
        self.view.customerTable.setRowCount(0)  # Limpiar tabla antes de cargar datos

        for row, data in enumerate(clientes):
            self.view.customerTable.insertRow(row)
            rowData = list(data.values())

            for col, item in enumerate(rowData):
                if not isinstance(item, str):
                    item = str(item)
                self.view.customerTable.setItem(row, col, QTableWidgetItem(item))

        self.view.customerTable.setSortingEnabled(True)
        self.view.customerTable.resizeColumnsToContents()

    def update_customer(self):
        cliente_data = {
            "nombre": self.view.customerName.text(),
            "apellido_paterno": self.view.customerLastPaternalName.text(),
            "apellido_materno": self.view.customerLastMaternalName.text(),
            "direccion": self.view.customerAddress.text(),
            "telefono": self.view.customerPhone.text(),
        }
        self.model.actualizar_cliente(self.getIDFromTable(self.view.customerTable), cliente_data);
        self.loadData()

    def delete_customer(self):
        self.model.eliminar_cliente(self.getIDFromTable(self.view.customerTable));
        self.loadData()
    
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