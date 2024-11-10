from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget
from PyQt5 import QtCore

from Model.date_model import CitaModel

from datetime import datetime

import pywhatkit as pw

class CitaController:
    def __init__(self, main_window):
        self.model = CitaModel()
        self.view = main_window

        # Conectar botones/señales
        self.view.addDate.clicked.connect(self.add_date)
        self.view.updateDate.clicked.connect(self.update_date)
        self.view.deleteDate.clicked.connect(self.delete_date)
        self.view.dateTable.currentCellChanged.connect(self.setDataOnWidgets)
        
    def add_date(self):
        fecha_cita_str = self.view.dateDates.date().toString("yyyy-MM-dd")
        date_data = {
            "descripcion": self.view.dateDescription.text(),
            "fecha": fecha_cita_str,
            "id_cliente": self.model.obtener_id_cliente(self.view.dateCustomer.currentText())
        }
        self.model.agregar_cita(date_data)
        numero = f"+52 {self.model.obtener_tel_cliente(self.view.dateCustomer.currentText())}"
        mensaje = f"La cita para {self.view.dateDescription.text()} con fecha del {fecha_cita_str}"
        try:
            # Enviar el mensaje

            pw.sendwhatmsg_instantly(numero, mensaje, tab_close=True)
            print("Mensaje Enviado")
        except Exception as e:
            print(f"Ocurrió un error al enviar el mensaje: {e}")
        self.loadData()
        
    def loadData(self):
        citas = self.model.obtener_citas()
        self.view.dateTable.setRowCount(0)  # Limpiar tabla antes de cargar datos
        clientes = self.model.obtener_clientes()
        clientesBox = [item['nombre'] for item in clientes]
        self.view.dateCustomer.clear()
        self.view.dateCustomer.addItems(clientesBox)
        for row, data in enumerate(citas):
            self.view.dateTable.insertRow(row)
            rowData = list(data.values())

            for col, item in enumerate(rowData):
                if not isinstance(item, str):
                    item = str(item)
                self.view.dateTable.setItem(row, col, QTableWidgetItem(item))

        self.view.dateTable.setSortingEnabled(True)
        self.view.dateTable.resizeColumnsToContents()

    def update_date(self):
        fecha_cita_str = self.view.dateDates.date().toString("yyyy-MM-dd")
        date_data = {
            "descripcion": self.view.dateDescription.text(),
            "fecha": fecha_cita_str,
            "id_cliente": self.model.obtener_id_cliente(self.view.dateCustomer.currentText())
        }
        self.model.actualizar_cita(self.getIDFromTable(self.view.dateTable), date_data);
        self.loadData()

    def delete_date(self):
        self.model.eliminar_cita(self.getIDFromTable(self.view.dateTable));
        self.loadData()
    
    def setDataOnWidgets(self, row, col):
        if row == -1 or col == -1:
            # Limpia cada campo de entrada directamente
            self.view.dateDescription.setText("")
            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d")
            qdate = QtCore.QDate.fromString(now_str, "yyyy-MM-dd")
            self.view.dateDates.setDate(qdate)
            self.view.dateCustomer.setCurrentIndex(0)
            return
        
        data = self.getDataFromTable(self.view.dateTable)
        
        self.view.dateDescription.setText(data[0])
        col_to_date = datetime.strptime(data[1], "%Y-%m-%d")
        col_str = col_to_date.strftime("%Y-%m-%d")
        qdate = QtCore.QDate.fromString(col_str, "yyyy-MM-dd")
        self.view.dateDates.setDate(qdate)
        index = self.view.dateCustomer.findText(data[2])
        if index == -1:
            self.view.dateCustomer.addItem(data[2])
            index = self.view.dateCustomer.count() - 1
        self.view.dateCustomer.setCurrentIndex(index)
        
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