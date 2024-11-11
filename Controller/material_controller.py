from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget

from Model.material_model import MaterialModel

from datetime import datetime
import pywhatkit as pw

class MaterialController:
    def __init__(self, main_window, rem):
        self.model = MaterialModel()
        self.view = main_window
        self.rem = rem

        # Conectar botones/señales
        self.view.addMaterial.clicked.connect(self.add_material)
        self.view.updateMaterial.clicked.connect(self.update_material)
        self.view.deleteMaterial.clicked.connect(self.delete_material)
        self.view.materialTable.currentCellChanged.connect(self.setDataOnWidgets)
        
    def add_material(self):
        material_data = {
            "nombre": self.view.materialName.text(),
            "cantidad": self.view.materialCant.text(),
            "id_proveedor": self.model.obtener_id_proveedor(self.view.materialProv.currentText())
        }
        self.model.agregar_material(material_data)
        
        #ENVIA MENSAJE Y AÑADE EL MENSAJE PARA EL BD
        numero = f"+52 {self.model.obtener_tel_proveedor(self.view.materialProv.currentText())}"
        mensaje = f"Necesito {self.view.materialCant.text()} de {self.view.materialName.text()}"
        fecha_y_hora_actuales = datetime.now()
        fecha_y_hora = fecha_y_hora_actuales.strftime('%Y/%m/%d %H:%M:%S')
        msg_data = {
            "remitente": self.rem,
            "destinatario": self.view.materialProv.currentText(),
            "fecha": fecha_y_hora,
            "mensaje": mensaje
        }
        try:
            # Enviar el mensaje
            pw.sendwhatmsg_instantly(numero, mensaje, tab_close=True)
            print("Mensaje Enviado")
            self.model.agregar_mensaje(msg_data)
        except Exception as e:
            print(f"Ocurrió un error al enviar el mensaje: {e}")
        self.loadData()

    def loadData(self):
        materiales = self.model.obtener_materiales()
        self.view.materialTable.setRowCount(0)  # Limpiar tabla antes de cargar datos
        prooveedores = self.model.obtener_proveedores()
        proveedoresBox = [item['nombre'] for item in prooveedores]
        self.view.materialProv.clear()
        self.view.materialProv.addItems(proveedoresBox)
        for row, data in enumerate(materiales):
            self.view.materialTable.insertRow(row)
            rowData = list(data.values())

            for col, item in enumerate(rowData):
                if not isinstance(item, str):
                    item = str(item)
                self.view.materialTable.setItem(row, col, QTableWidgetItem(item))

        self.view.materialTable.setSortingEnabled(True)
        self.view.materialTable.resizeColumnsToContents()

    def update_material(self):
        material_data = {
            "nombre": self.view.materialName.text(),
            "cantidad": self.view.materialCant.text(),
            "id_proveedor": self.model.obtener_id_proveedor(self.view.materialProv.currentText())
        }
        self.model.actualizar_material(self.getIDFromTable(self.view.materialTable), material_data);
        self.loadData()

    def delete_material(self):
        self.model.eliminar_material(self.getIDFromTable(self.view.materialTable));
        self.loadData()
    
    def setDataOnWidgets(self, row, col):
        if row == -1 or col == -1:
            # Limpia cada campo de entrada directamente
            self.view.materialName.setText("")
            self.view.materialCant.setText("")
            self.view.materialProv.setCurrentIndex(0)
            return
        
        data = self.getDataFromTable(self.view.materialTable)
        
        self.view.materialName.setText(data[0])
        self.view.materialCant.setText(data[1])
        index = self.view.materialProv.findText(data[2])
        if index == -1:
            self.view.materialProv.addItem(data[2])
            index = self.view.materialProv.count() - 1
        self.view.materialProv.setCurrentIndex(index)
        
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