from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStatusBar
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QFont
import cv2
import numpy as np
from core.cloak import create_mask, apply_cloak_effect
from core.capture import capture_background, is_lighting_good
from core.utils import text_to_speech

class CloakApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧥 Invisible Cloak - PyQt5 Edition")

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.background = None
        self.lower_blue = np.array([90, 50, 50])
        self.upper_blue = np.array([130, 255, 255])

        # UI Elements
        self.image_label = QLabel()
        self.image_label.setFixedSize(1100, 800)
        self.setFixedSize(1100, 800)
        self.image_label.setStyleSheet("background-color: black;")

        self.status_bar = QStatusBar()
        self.status_bar.setFixedHeight(50)
        self.status_bar.showMessage("Welcome to the Invisible Cloak App!")

        self.start_button = QPushButton("▶ Start Cloak")
        self.reset_button = QPushButton("🔄 Reset Background")
        self.exit_button = QPushButton("❌ Exit")

        for btn in [self.start_button, self.reset_button, self.exit_button]:
            btn.setMinimumHeight(40)
            btn.setFont(QFont("Arial", 12))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.exit_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.status_bar)
        self.setLayout(main_layout)

        self.start_button.clicked.connect(self.start_cloak)
        self.reset_button.clicked.connect(self.capture_background)
        self.exit_button.clicked.connect(self.close_app)

        self.capture_background()

    def capture_background(self):
        self.background = capture_background(self.cap, self.status_bar)

    def start_cloak(self):
        if self.background is None:
            self.status_bar.showMessage("❌ Please capture background first.")
            return
        self.status_bar.showMessage("🧥 Cloak effect running...")
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.status_bar.showMessage("⚠ Could not read frame from webcam.")
            return

        frame = cv2.flip(frame, 1)
        mask = create_mask(frame, self.lower_blue, self.upper_blue)
        result = apply_cloak_effect(frame, mask, self.background)
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

        qt_img = QImage(result_rgb.data, result_rgb.shape[1], result_rgb.shape[0],
                        result_rgb.shape[1] * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img).scaled(
            self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.image_label.setPixmap(pixmap)

    def close_app(self):
        self.status_bar.showMessage("Exiting...")
        self.timer.stop()
        self.cap.release()
        cv2.destroyAllWindows()
        self.close()
