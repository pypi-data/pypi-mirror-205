from dataclasses import dataclass
from typing import Any


@dataclass
class PropertyValue:
    value: Any


class PropertyHAlign(PropertyValue):

    def __init__(self, value):
        super().__init__(value)

        if self.value == 'left':
            self.value = 0
        elif self.value == 'center':
            self.value = 1
        elif self.value == 'right':
            self.value = 2
        else:
            raise ValueError(f"Unknown value « {self.value} » for PropertyHAlign type")


class PropertyVAlign(PropertyValue):

    def __init__(self, value):
        super().__init__(value)

        if self.value == 'top':
            self.value = 0
        elif self.value == 'middle':
            self.value = 1
        elif self.value == 'bottom':
            self.value = 2
        else:
            raise ValueError(f"Unknown value « {self.value} » for PropertyVAlign type")
