import uno
import unohelper

from com.sun.star.lang import XComponent
from com.sun.star.ui import LayoutSize, UIElementType, XSidebarPanel, XUIElement, XToolPanel


class XUIPanel(unohelper.Base, XSidebarPanel, XUIElement, XToolPanel, XComponent):

    def __init__(self, ctx, x_frame, x_parent_window, url, minimal_width=None, dialog_url=""):
        self.ctx = ctx
        self.xParentWindow = x_parent_window
        self.height = 100
        self._frame = x_frame
        self._resource_url = url
        self._minimal_width = minimal_width if minimal_width is not None else 300
        self._type = UIElementType.TOOLPANEL
        self.dialog_url = dialog_url
        self._window = None

    def getRealInterface(self) -> 'XUIPanel':
        if not self._window:
            s_manager = self.ctx.ServiceManager

            provider = s_manager.createInstanceWithContext("com.sun.star.awt.ContainerWindowProvider", self.ctx)
            self._window = provider.createContainerWindow(self.dialog_url, "", self.xParentWindow, None)

        return self

    @property
    def Frame(self):
        return self._frame

    @property
    def ResourceURL(self) -> str:
        return self._resource_url

    @property
    def Type(self) -> int:
        return self._type

    # XComponent
    def dispose(self):
        pass

    def addEventListener(self, ev):
        pass

    def removeEventListener(self, ev): pass

    def createAccessible(self, i_parent_accessible):
        return self.Window

    @property
    def Window(self):
        return self._window

    # XSidebarPanel
    def getHeightForWidth(self, width):
        # print("getHeightForWidth: %s" % width)
        # return LayoutSize(0, -1, 0) # full height
        return LayoutSize(self.height, self.height, self.height)

    # LO 5.1+
    def getMinimalWidth(self):
        return self._minimal_width
