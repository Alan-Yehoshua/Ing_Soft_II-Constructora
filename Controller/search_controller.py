from PyQt5.QtWidgets import QTableWidgetItem

from Model.search_model import BusquedaModel

class BusquedaController:
    def __init__(self, main_window):
        self.model = BusquedaModel()
        self.view = main_window
        
        self.view.Filter.currentIndexChanged.connect(self.toggle_filters)
        self.view.Search.clicked.connect(self.update_table)
        
        self.active_filter = None
        
    def toggle_filters(self):
        self.view.searchTable.setRowCount(0)
        current_filter = self.view.Filter.currentText()
        self.active_filter = current_filter
        self.set_table_headers()
        
    def set_table_headers(self):
        headers = []
        if self.active_filter == "cliente":
            self.view.toSearch.setPlaceholderText("Nombre")
            headers = ["ID Cliente", "Nombre", "ApellidoP", "ApellidoM", "Direccion", "Telefono"]
        
        elif self.active_filter == "citas":
            self.view.toSearch.setPlaceholderText("Descripcion")
            headers = ["ID Cita", "Descripción", "Fecha", "ID Cliente"]
        
        elif self.active_filter == "material":
            self.view.toSearch.setPlaceholderText("Nombre")
            headers = ["ID Material", "Nombre", "Cantidad", "ID Proveedor"]
        
        elif self.active_filter == "proveedor":
            self.view.toSearch.setPlaceholderText("Nombre")
            headers = ["ID Proveedor", "Nombre", "Teléfono"]
        
        elif self.active_filter == "mensajes_enviados":
            self.view.toSearch.setPlaceholderText("Remitente")
            headers = ["ID", "Origen", "Destino", "Fecha_Hora", "Mensaje"]
        
        elif self.active_filter == "obra":
            self.view.toSearch.setPlaceholderText("Nombre")
            headers = ["ID Obra", "Nombre", "Dirección", "Fecha de Inicio", "ID Cliente"]
        
        elif self.active_filter == "empleados":
            self.view.toSearch.setPlaceholderText("Nombre")
            headers = ["ID Empleado", "Nombre", "ApellidoP", "ApellidoM", "Email", "Puesto", "Usuario", "Contraseña", "Id_obra"]

        self.view.searchTable.setColumnCount(len(headers))
        self.view.searchTable.setHorizontalHeaderLabels(headers)
        
    def update_table(self):
        self.view.searchTable.setRowCount(0)
        data = []
        if self.active_filter == "cliente":
            data = self.model.obtener_clientes(self.view.toSearch.text())
        elif self.active_filter == "citas":
            data = self.model.obtener_citas(self.view.toSearch.text())
        elif self.active_filter == "material":
            data = self.model.obtener_materiales(self.view.toSearch.text())
        elif self.active_filter == "proveedor":
            data = self.model.obtener_Proveedores(self.view.toSearch.text())
        elif self.active_filter == "obra":
            data = self.model.obtener_Obras(self.view.toSearch.text())
        elif self.active_filter == "empleados":
            data = self.model.obtener_empleados(self.view.toSearch.text())
        elif self.active_filter == "mensajes_enviados":
            data = self.model.obtener_mensajes(self.view.toSearch.text())
            
        for row_idx, row_data in enumerate(data):
            self.view.searchTable.insertRow(row_idx)
            rowData = list(row_data.values())
            for col_idx, item in enumerate(rowData):
                if not isinstance(item, str):
                    item = str(item)
                self.view.searchTable.setItem(row_idx, col_idx, QTableWidgetItem(item))
        self.view.Filter.setEnabled(True)
        
        self.view.searchTable.setSortingEnabled(True)
        self.view.searchTable.resizeColumnsToContents()