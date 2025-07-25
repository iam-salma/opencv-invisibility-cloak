import qdarkstyle
from PyQt5.QtWidgets import QApplication

def apply_dark_theme(app: QApplication):
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
