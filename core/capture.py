import cv2
import numpy as np
import time
from .utils import text_to_speech

def is_lighting_good(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean_brightness = gray.mean()
    return 100 < mean_brightness < 300

def capture_background(cap, status_bar):
    status_bar.showMessage("Capturing background... Please move out of the frame.")
    text_to_speech("Capturing background. Please move out of the frame.")
    time.sleep(2)

    backgrounds = []
    for _ in range(60):
        ret, frame = cap.read()
        if not ret:
            continue
        if not is_lighting_good(frame):
            text_to_speech("Lighting conditions are poor. Please adjust lighting.")
            continue
        backgrounds.append(np.flip(frame, axis=1))
        time.sleep(0.05)

    if backgrounds:
        text_to_speech("Background captured successfully.")
        status_bar.showMessage("✅ Background captured. Wear your cloak!")
        return np.mean(backgrounds, axis=0).astype(np.uint8)
    else:
        text_to_speech("Failed to capture background.")
        status_bar.showMessage("❌ Failed to capture background.")
        return None
