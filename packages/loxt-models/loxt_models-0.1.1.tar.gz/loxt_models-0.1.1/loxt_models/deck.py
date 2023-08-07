import uno
import unohelper
from com.sun.star.ui import XUIElementFactory
import pathlib

import loxt_models.panel
from loxt_models import panel as loxt_panel, x_ui_panel
from loxt_models.utils import message_box


class DeckModel(unohelper.Base, XUIElementFactory):
    EXTENSION_IDENTIFIER: str
    NAME: str
    PANEL_FACTORY: str
    ICON: pathlib.Path = None
    CONTEXT: str = 'any, any, visible ;'
    MINIMAL_WIDTH: int = 300

    title: str = ''

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        cls.PANEL_FACTORY = f"{cls.NAME}PanelFactory"

    def __init__(self, ctx=None):

        self.ctx = ctx
        self.panels = list()

        # add panels
        for attr in dir(self):
            if isinstance(getattr(self, attr), loxt_panel.PanelModel):
                self.panels.append(getattr(self, attr))

    @classmethod
    @property
    def panel_implementations(cls) -> dict[str, type[loxt_panel.PanelModel]]:
        return {
            f"private:resource/toolpanel/{cls.PANEL_FACTORY}/{getattr(cls, attr).NAME}": getattr(cls, attr).__class__
            for attr in dir(cls)
            if attr != 'panel_implementations' and isinstance(getattr(cls, attr), loxt_panel.PanelModel)}

    def createUIElement(self, url, args) -> x_ui_panel.XUIPanel:

        x_parent_window = None
        x_frame = None

        for arg in args:
            if arg.Name == "Frame":
                x_frame = arg.Value
            elif arg.Name == "ParentWindow":
                x_parent_window = arg.Value

        x_ui_element = x_ui_panel.XUIPanel(ctx=self.ctx,
                                           x_frame=x_frame,
                                           x_parent_window=x_parent_window,
                                           url=url,
                                           minimal_width=self.MINIMAL_WIDTH,
                                           dialog_url=f"vnd.sun.star.extension://{self.EXTENSION_IDENTIFIER}/Dialog.xdl"
                                           )

        # getting the real panel window
        # for setting the content
        panel_win = x_ui_element.getRealInterface().Window

        # panelWin has to be set visible
        panel_win.Visible = True
        _panel = self.show_panel(panel_win, url)

        # try to set height according to panel height - top : 13
        x_ui_element.height = 2_000

        return x_ui_element

    def show_panel(self, panel_win, url) -> loxt_models.panel.PanelModel:

        # url is set in Sidebar.xcu
        if url in self.panel_implementations.keys():
            panel_cls: type[loxt_panel.PanelModel] = self.panel_implementations[url]
            _panel = panel_cls(uno_context=self.ctx, dialog_container=panel_win)
            _panel.show()

            return _panel
