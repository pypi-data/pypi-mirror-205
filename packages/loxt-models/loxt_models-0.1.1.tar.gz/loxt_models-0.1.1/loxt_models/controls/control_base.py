from typing import Callable

from loxt_models.controls import property_value as pv
from loxt_models.listeners import action_listener
from loxt_models.utils import message_box


class ControlBase:

    INSTANCE_NAME: str

    def __init__(self, name: str, tab_index: int = 0,
                 x: int = 0, y: int = 0,
                 width: int = 50, height: int = 16,
                 ):

        self._instance = None
        self._connect: dict[str: Callable] = dict()

        self.Name = pv.PropertyValue(name)
        self.TabIndex = pv.PropertyValue(tab_index)
        self.PositionX = pv.PropertyValue(str(x))
        self.PositionY = pv.PropertyValue(str(y))
        self.Width = pv.PropertyValue(width)
        self.Height = pv.PropertyValue(height)

    def create_instance(self, dialog_model):
        self._instance = dialog_model.createInstance(self.INSTANCE_NAME)

        for attr in dir(self):
            if isinstance(getattr(self, attr), pv.PropertyValue):
                setattr(self._instance, attr, getattr(self, attr).value)

    def connect(self, **kwargs):
        for key, value in kwargs.items():
            if not isinstance(key, str) or not key.startswith('on_'):
                raise ValueError("connect argument name must be a string starting with 'on_'")
            elif not callable(value):
                raise ValueError("connect argument value must a callable")
            else:
                self._connect[key] = value

    @property
    def connections(self):
        return self._connect

    @property
    def instance(self):
        return self._instance
