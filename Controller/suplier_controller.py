from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from Model.suplier_model import ProveedorModel

class ProveedorController:
    def __init__(self, main_window):
        self.model = ProveedorModel()
        self.view = main_window

        # Conectar señales
        self.view.addSuplier.clicked.connect(self.add_customer)
        self.view.updateSuplier.clicked.connect(self.update_customer)
        self.view.deleteSuplier.clicked.connect(self.delete_customer)
        self.view.suplierTable.currentCellChanged.connect(self.setDataOnWidgets)
        
    def add_customer(self):
        proveedor_data = {
            "nombre": self.view.suplierName.text(),
            "telefono": self.view.suplierNumber.text(),
        }
        self.model.agregar_Proveedores(proveedor_data)
        self.loadData()

    #CARGAR DATOS DE TODOS LAS TABLAS
    def loadData(self):
        proveedores = self.model.obtener_Proveedores()
        self.view.suplierTable.setRowCount(0)  # Limpiar tabla antes de cargar datos

        for row, data in enumerate(proveedores):
            self.view.suplierTable.insertRow(row)
            rowData = list(data.values())

            for col, item in enumerate(rowData):
                if not isinstance(item, str):
                    item = str(item)
                self.view.suplierTable.setItem(row, col, QTableWidgetItem(item))

        self.view.suplierTable.setSortingEnabled(True)
        self.view.suplierTable.resizeColumnsToContents()

    def update_customer(self):
        proveedor_data = {
            "nombre": self.view.suplierName.text(),
            "telefono": self.view.suplierNumber.text(),
        }
        self.model.actualizar_Proveedores(self.getIDFromTable(self.view.suplierTable), proveedor_data);
        self.loadData()

    def delete_customer(self):
        self.model.eliminar_Proveedores(self.getIDFromTable(self.view.suplierTable));
        self.loadData()
    
    def setDataOnWidgets(self, row, col):
        if row == -1 or col == -1:
            # Limpia cada campo de entrada directamente
            self.view.suplierName.setText("")
            self.view.suplierNumber.setText("")
            return
        
        data = self.getDataFromTable(self.view.suplierTable)
        
        self.view.suplierName.setText(data[0])
        self.view.suplierNumber.setText(data[1])
        
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