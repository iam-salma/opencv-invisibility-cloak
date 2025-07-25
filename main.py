from PyQt5.QtWidgets import QApplication
import sys
from ui.window import CloakApp
from styles.dark_theme import apply_dark_theme

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        apply_dark_theme(app)
    except ImportError:
        pass

    window = CloakApp()
    window.show()
    sys.exit(app.exec_())
