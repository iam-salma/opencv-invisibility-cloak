from PyQt5.QtWidgets import QApplication
import sys
from ui.window import CloakApp

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        import qdarkstyle
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except ImportError:
        pass

    window = CloakApp()
    window.show()
    sys.exit(app.exec_())
