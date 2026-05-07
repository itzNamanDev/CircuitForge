"""Lightweight pluggable symbol detector.

This v1 detector uses contour heuristics for clean textbook circuits and is kept
modular so it can be swapped with a trained detector later.
"""
from __future__ import annotations
import cv2
import numpy as np
from circuitforge.common.models import DetectedComponent


def detect_symbols(thresh_img: np.ndarray) -> list[DetectedComponent]:
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected: list[DetectedComponent] = []
    idx = 0
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        if area < 70:
            continue
        aspect = w / max(h, 1)
        if area < 120 and 0.8 < aspect < 1.2:
            kind = "AM"  # tiny circular marks treated as meter/junction candidate in v1
        elif aspect > 2.3:
            kind = "R"
        elif aspect < 0.5:
            kind = "VDC"
        else:
            kind = "C"
        orientation = "h" if w >= h else "v"
        terminals = ((x, y + h // 2), (x + w, y + h // 2)) if orientation == "h" else ((x + w // 2, y), (x + w // 2, y + h))
        detected.append(DetectedComponent(
            component_id=f"X{idx}", kind=kind, bbox=(x, y, w, h), confidence=0.6,
            terminal_points=terminals, orientation=orientation
        ))
        idx += 1
    return sorted(detected, key=lambda d: d.bbox[0])
