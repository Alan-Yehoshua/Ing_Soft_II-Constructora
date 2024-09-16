from PyQt5.QtWidgets import QApplication, QStyleFactory
from login import Login
import sys

app = QApplication(sys.argv)
app.setStyle(QStyleFactory.create('fusion'))

window = Login()
window.show()

sys.exit(app.exec())