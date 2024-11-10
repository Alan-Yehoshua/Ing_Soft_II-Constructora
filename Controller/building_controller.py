from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget
from PyQt5 import QtCore

from Model.building_model import ObraModel

from datetime import datetime

class ObraController:
    def __init__(self, main_window):
        self.model = ObraModel()
        self.view = main_window

        # Conectar botones/señales
        self.view.addBuilding.clicked.connect(self.add_building)
        self.view.updateBuilding.clicked.connect(self.update_building)
        self.view.deleteBuilding.clicked.connect(self.delete_building)
        self.view.buildingTable.currentCellChanged.connect(self.setDataOnWidgets)
        
    def add_building(self):
        fecha_inicio_str = self.view.buildingDate.date().toString("yyyy-MM-dd")
        obra_data = {
            "nombre": self.view.buildingProyect.text(),
            "ubicacion": self.view.buildingAddress.text(),
            "fecha_inicio": fecha_inicio_str,
            "id_cliente": self.model.obtener_id_cliente(self.view.buildingCustomer.currentText())
        }
        self.model.agregar_obra(obra_data)
        self.loadData()

    def loadData(self):
        obras = self.model.obtener_Obras()
        self.view.buildingTable.setRowCount(0)  # Limpiar tabla antes de cargar datos
        clientes = self.model.obtener_clientes()
        clienteBox = [item['nombre'] for item in clientes]
        self.view.buildingCustomer.clear()
        self.view.buildingCustomer.addItems(clienteBox)
        for row, data in enumerate(obras):
            self.view.buildingTable.insertRow(row)
            rowData = list(data.values())

            for col, item in enumerate(rowData):
                if not isinstance(item, str):
                    item = str(item)
                self.view.buildingTable.setItem(row, col, QTableWidgetItem(item))

        self.view.buildingTable.setSortingEnabled(True)
        self.view.buildingTable.resizeColumnsToContents()

    def update_building(self):
        fecha_inicio_str = self.view.buildingDate.date().toString("yyyy-MM-dd")
        building_data = {
            "nombre": self.view.buildingProyect.text(),
            "ubicacion": self.view.buildingAddress.text(),
            "fecha_inicio": fecha_inicio_str,
            "id_cliente": self.model.obtener_id_cliente(self.view.buildingCustomer.currentText())
        }
        self.model.actualizar_obra(self.getIDFromTable(self.view.buildingTable), building_data);
        self.loadData()

    def delete_building(self):
        self.model.eliminar_obra(self.getIDFromTable(self.view.buildingTable));
        self.loadData()
    
    def setDataOnWidgets(self, row, col):
        if row == -1 or col == -1:
            # Limpia cada campo de entrada directamente
            self.view.buildingProyect.setText("")
            self.view.buildingAddress.setText("")
            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d")
            qdate = QtCore.QDate.fromString(now_str, "yyyy-MM-dd")
            self.view.buildingDate.setDate(qdate)
            self.view.buildingCustomer.setCurrentIndex(0)
            return
        
        data = self.getDataFromTable(self.view.buildingTable)
        
        self.view.buildingProyect.setText(data[0])
        self.view.buildingAddress.setText(data[1])
        col_to_date = datetime.strptime(data[2], "%Y-%m-%d")
        col_str = col_to_date.strftime("%Y-%m-%d")
        qdate = QtCore.QDate.fromString(col_str, "yyyy-MM-dd")
        self.view.buildingDate.setDate(qdate)
        index = self.view.buildingCustomer.findText(data[3])
        if index == -1:
            self.view.buildingCustomer.addItem(data[3])
            index = self.view.buildingCustomer.count() - 1
        self.view.buildingCustomer.setCurrentIndex(index)
        
    def getDataFromTable(self, table: QTableWidget):
        row = table.currentRow()
        data = []
    
        for col in range(table.columnCount()):
            if col == 0:
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