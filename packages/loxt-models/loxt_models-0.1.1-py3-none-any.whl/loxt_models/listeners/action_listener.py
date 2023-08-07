import uno
import unohelper

from com.sun.star.awt import XActionListener


class ActionListener(unohelper.Base, XActionListener):
    def __init__(self, action):
        self.action = action

    def actionPerformed(self, event):
        if self.action is not None:
            return self.action(event)
        else:
            pass

    def disposing(self, event):
        pass
