import cv2
import numpy as np

def create_mask(frame, lower_blue, upper_blue):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask = cv2.erode(mask, kernel, iterations=1)
    return mask

def apply_cloak_effect(frame, mask, background):
    mask = mask.astype(np.float32) / 255.0
    mask = cv2.merge([mask, mask, mask])
    mask_inv = 1.0 - mask
    frame = frame.astype(np.float32)
    background = background.astype(np.float32)
    return (frame * mask_inv + background * mask).astype(np.uint8)
