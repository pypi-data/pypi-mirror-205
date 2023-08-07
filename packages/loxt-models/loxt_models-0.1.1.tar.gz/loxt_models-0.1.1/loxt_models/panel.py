from typing import Union, Optional

import uno
import unohelper
from com.sun.star.awt import XActionListener, XWindowListener, PosSize
from com.sun.star.task import XJobExecutor

from loxt_models import deck as loxt_deck
from loxt_models.controls import control_base
from loxt_models.listeners.action_listener import ActionListener
from loxt_models.utils import message_box


class PanelModel(unohelper.Base, XActionListener, XWindowListener, XJobExecutor):
    NAME: Union[str, None] = None
    ORDER_INDEX: int
    CONTEXT: str = 'any, any, visible ;'

    title: str = ''
    wants_canvas: bool = False

    _height: int = 196

    def __init__(self, uno_context=None, dialog_container=None):

        if self.NAME is None:
            self.NAME = self.__class__.__name__

        if not self.title:
            self.title = self.NAME

        self.FACTORY_NAME: str = f"{self.NAME}Factory"
        self.IMPLEMENTATION_URL: str = f"private:resource/toolpanel/{self.FACTORY_NAME}/{self.NAME}"
        # self.deck: Optional[loxt_deck.DeckModel] = None

        if uno_context is not None:
            # execute _pre_init method
            self._pre_init()

            self.LocalContext = uno_context
            self.ServiceManager = self.LocalContext.ServiceManager
            self.Toolkit = self.ServiceManager.createInstanceWithContext("com.sun.star.awt.ExtToolkit",
                                                                         self.LocalContext)

            self.DialogContainer = dialog_container

            self.DialogModel = self.ServiceManager.createInstance("com.sun.star.awt.UnoControlDialogModel")
            self.DialogContainer.setModel(self.DialogModel)
            self.DialogModel.Name = self.NAME
            self.DialogModel.PositionX = "0"
            self.DialogModel.PositionY = "0"
            self.DialogModel.Width = 100
            self.DialogModel.Height = 100
            self.DialogModel.Closeable = True
            self.DialogModel.Moveable = True
            self.DialogModel.Title = self.title

            # Add controls defined as class attributes
            for attr in dir(self):
                if isinstance(getattr(self, attr, None), control_base.ControlBase):
                    _control: control_base.ControlBase = getattr(self, attr)
                    _control.create_instance(self.DialogModel)
                    # setattr(self, attr, _control.instance)
                    self.DialogModel.insertByName(_control.instance.Name, _control.instance)

                    # connect callbacks to controls
                    if getattr(_control, '_connect', None) is not None:

                        control_instance = self.DialogContainer.getControl(_control.instance.Name)

                        for slot, callback in _control.connections.items():

                            if slot == 'on_click':
                                listener = ActionListener(callback)
                                control_instance.addActionListener(listener)

                    # Convert class attribute to control view instance
                    setattr(self, attr, self.DialogContainer.getControl(_control.instance.Name))

            self.DialogContainer.addWindowListener(self)

    def _pre_init(self):
        pass

    def actionPerformed(self, event):
        pass

    def resize_controls(self, dialog):
        pass

    def windowResized(self, event):
        self.resize_controls(dialog=event.Source)

    def show(self):
        self.DialogContainer.setVisible(True)
        self.DialogContainer.createPeer(self.Toolkit, None)
        self.DialogContainer.execute()

    @property
    def height(self):
        return self.DialogContainer.getPosSize()

    @height.setter
    def height(self, value):
        self.DialogContainer.setPosSize(0, 0, 0, value, PosSize.HEIGHT)
