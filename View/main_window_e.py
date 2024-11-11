from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from Controller.customer_controller import ClienteController
from Controller.suplier_controller import ProveedorController
from Controller.material_controller import MaterialController
from Controller.search_controller import BusquedaController

class MainWindowE(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("C:/Python_code/Ing_Soft_II_Constrcutora/View/HomePageEmployee.ui", self)
        #LLAMADA A LOS CONTROLADORES
        customer_controller = ClienteController(self)
        suplier_controller = ProveedorController(self)
        material_controller = MaterialController(self)
        search_controller = BusquedaController(self)
        
        self.controllerCliente = customer_controller
        self.controllerSuplier = suplier_controller
        self.controllerMaterial = material_controller
        self.controllerBusqeuda = search_controller
        
        #CARGAR DATOS
        self.controllerCliente.loadData()
        self.controllerSuplier.loadData()
        self.controllerMaterial.loadData()
        
        self.customerButton.clicked.connect(self.customerPage)
        self.supplierButton.clicked.connect(self.supplierPage)
        self.materialButton.clicked.connect(self.materialPage)
        self.requestButton.clicked.connect(self.requestPage)
        
    def customerPage(self):
        self.stackedWidget.setCurrentIndex(0)
    def supplierPage(self):
        self.stackedWidget.setCurrentIndex(2)
    def materialPage(self):
        self.stackedWidget.setCurrentIndex(4)
    def requestPage(self):
        self.stackedWidget.setCurrentIndex(6)

