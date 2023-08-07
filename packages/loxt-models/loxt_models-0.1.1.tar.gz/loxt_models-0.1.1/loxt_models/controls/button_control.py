from typing import Callable

from loxt_models.controls import control_base
from loxt_models.controls import property_value as pv


class ButtonControl(control_base.ControlBase):

    INSTANCE_NAME = "com.sun.star.awt.UnoControlButtonModel"

    def __init__(self, name: str, tab_index: int = 0,
                 x: int = 0, y: int = 0,
                 width: int = 50, height: int = 16,
                 label: str = '',
                 align: str = 'left', v_align: str = 'middle',
                 on_click: Callable = None,
                 ):

        super().__init__(name, tab_index, x, y, width, height)

        self.Label = pv.PropertyValue(label)
        self.Align = pv.PropertyHAlign(align)
        self.VerticalAlign = pv.PropertyVAlign(v_align)

        self._on_click = on_click
