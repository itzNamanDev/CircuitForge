"""OpenCV preprocessing stage.

Improves image quality before detection: grayscale, denoising, thresholding,
edge extraction, line extraction, junction candidate detection, crop cleanup.
"""
from __future__ import annotations
import cv2
import numpy as np


def preprocess_image(image: np.ndarray) -> dict[str, np.ndarray]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 3)
    edges = cv2.Canny(thresh, 30, 120)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=35, minLineLength=20, maxLineGap=6)

    kernel = np.ones((3, 3), np.uint8)
    junction_map = cv2.dilate(thresh, kernel, iterations=1)
    # Crop to non-empty foreground region.
    ys, xs = np.where(thresh > 0)
    if len(xs) and len(ys):
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        cropped = image[y0:y1 + 1, x0:x1 + 1]
    else:
        cropped = image

    return {
        "gray": gray,
        "denoised": denoised,
        "thresh": thresh,
        "edges": edges,
        "lines": lines if lines is not None else np.empty((0, 1, 4), dtype=int),
        "junction_map": junction_map,
        "cropped": cropped,
    }
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 2)
    edges = cv2.Canny(thresh, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=30, minLineLength=15, maxLineGap=5)
    return {"gray": gray, "denoised": denoised, "thresh": thresh, "edges": edges, "lines": lines if lines is not None else np.empty((0,1,4), dtype=int)}
