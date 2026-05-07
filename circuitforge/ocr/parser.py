"""OCR parsing helpers.

Reads textual values and converts them into normalized SI magnitudes + units.
"""
from __future__ import annotations
import re

UNIT_SCALE = {"": 1.0, "k": 1e3, "m": 1e-3, "u": 1e-6, "n": 1e-9, "meg": 1e6}


def parse_value(text: str) -> tuple[float, str]:
    t = text.strip().lower().replace("ω", "ohm").replace("Ω", "ohm")
from __future__ import annotations
import re

UNIT_SCALE = {
    "": 1.0,
    "k": 1e3,
    "m": 1e-3,
    "u": 1e-6,
    "n": 1e-9,
    "meg": 1e6,
}

def parse_value(text: str) -> tuple[float, str]:
    t = text.strip().lower().replace("Ω", "ohm")
    m = re.search(r"([0-9]*\.?[0-9]+)\s*(meg|k|m|u|n)?\s*(ohm|f|h|v|a)?", t)
    if not m:
        raise ValueError(f"Cannot parse value: {text}")
    value = float(m.group(1)) * UNIT_SCALE.get(m.group(2) or "", 1.0)
    unit = m.group(3) or ""
    return value, unit
