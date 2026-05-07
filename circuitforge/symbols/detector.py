from __future__ import annotations
import cv2
import numpy as np
from circuitforge.common.models import DetectedComponent


def detect_symbols(thresh_img: np.ndarray) -> list[DetectedComponent]:
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected: list[DetectedComponent] = []
    for i, c in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        if area < 80:
            continue
        aspect = w / max(h, 1)
        kind = "R" if 1.5 < aspect < 4.5 else "VDC"
        detected.append(DetectedComponent(component_id=f"X{i}", kind=kind, bbox=(x, y, w, h), confidence=0.55))
    return detected
