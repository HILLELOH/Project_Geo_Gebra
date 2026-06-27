"""Alphanumeric label generator for geometry objects (A0, B0, … Z0, A1, …)."""
from __future__ import annotations
import re
import config


def get_label_parts(label: str) -> tuple:
    """Split 'B3' → ('B', '3'). Returns (label, False) if no digits."""
    match = re.search(r"\d", label)
    if match:
        idx = match.start()
        return label[:idx], label[idx:]
    return label, False


def generate_alphanumeric_sequence():
    """Infinite generator yielding unique shape labels, reusing deleted ones first."""
    current_char = "A"
    num_iteration = 0
    config.last_label_before_return = "A"
    config.last_turn_before_return = 0

    while True:
        if config.deleted_labels:
            tmp = config.deleted_labels.pop(0)
            chars, numbers = get_label_parts(tmp)
            if chars != config.last_label_before_return:
                yield chars + str(numbers)
            elif chars == "Z":
                yield chars + str(numbers)
                current_char = "A"
                num_iteration = numbers + 1
            else:
                yield current_char + str(num_iteration)
                current_char = chr(ord(config.last_label_before_return) + 1)
                num_iteration = numbers
        else:
            yield current_char + str(num_iteration)
            if current_char == "Z":
                current_char = "A"
                num_iteration += 1
            else:
                current_char = chr(ord(current_char) + 1)
