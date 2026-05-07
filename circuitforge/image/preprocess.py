from __future__ import annotations
import cv2
import numpy as np


def preprocess_image(image: np.ndarray) -> dict[str, np.ndarray]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 2)
    edges = cv2.Canny(thresh, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=30, minLineLength=15, maxLineGap=5)
    return {"gray": gray, "denoised": denoised, "thresh": thresh, "edges": edges, "lines": lines if lines is not None else np.empty((0,1,4), dtype=int)}
