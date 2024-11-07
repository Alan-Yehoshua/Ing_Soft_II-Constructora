from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore
from PyQt5.uic import loadUi

from Controller.customer_controller import ClienteController
from Controller.building_controller import ObraController
from Controller.employee_controller import EmpleadoController

from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("C:/Python_code/Ing_Soft_II_Constrcutora/View/HomePage.ui", self)
        #LLAMADA A LOS CONTROLADORES
        customer_controller = ClienteController(self)
        building_controller = ObraController(self)
        employe_controller = EmpleadoController(self);
        self.controllerCliente = customer_controller
        self.controllerObra = building_controller
        self.controllerEmpleado = employe_controller
        
        self.controllerCliente.loadData()
        self.controllerObra.loadData()
        self.controllerEmpleado.loadData()
        
        now = datetime.now()
        # Convertimos `now` a una cadena con el formato adecuado
        now_str = now.strftime("%Y-%m-%d")
        # Ahora pasamos la cadena a `fromString`
        qdate = QtCore.QDate.fromString(now_str, "yyyy-MM-dd")
        self.buildingDate.setDisplayFormat("yyyy-MM-dd")
        self.buildingDate.setDate(qdate)
        
        for val, btn in enumerate([self.customerButton, self.employeeButton, self.supplierButton,
                                   self.buildingButton, self.materialButton, self.dateButton, self.requestButton]):
            btn.toggled.connect(lambda checked, btn=val: self.changeWindow(btn) if checked else None)

    #CAMBIA ENTRE VENTANAS
    def changeWindow(self, index: int):
        self.stackedWidget.setCurrentIndex(index)
        
        # Bloqueo tempral debido a la cantidad de paginas en self.stackedWidget
        if index > 0:
            index = 0
        
        # Limpia la seleccion de las demás tablas
        for idx, table in enumerate([self.customerTable, self.employeeTable]):
            if idx == index: # Si los indices coinciden, se salta la iteración
                continue
            
            table.setSortingEnabled(False)
            table.clearSelection()