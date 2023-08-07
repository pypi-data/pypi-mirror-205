import uno
import unohelper

from com.sun.star.awt.MessageBoxType import MESSAGEBOX
from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK


def message_box(title, text, mb_type=MESSAGEBOX, buttons=BUTTONS_OK):
    ctx = uno.getComponentContext()
    sm = ctx.ServiceManager
    si = sm.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)
    toolkit = sm.createInstanceWithContext("com.sun.star.awt.ExtToolkit", ctx)
    message = si.createMessageBox(toolkit, mb_type, buttons, title, text)
    message.execute()
