from __future__ import annotations

from loxt_models import sidebar as loxt_sidebar


class ExtensionModel:

    NAME: str = None
    VERSION: str
    AUTHOR: str = 'author'
    IDENTIFIER_BASE: str = None
    IDENTIFIER: str = None
    PLATFORM: str = 'all'
    OOO_MINIMAL_VERSION: str = None
    OOO_MINIMAL_VERSION_NAME: str = None
    UPDATE_INFORMATION_SRC: str = None
    LICENSE_ACCEPT_BY: str = 'user'
    LICENSE_SUPPRESS_ON_UPDATE = None
    LICENSE_TXT_HREF: str = None
    PUBLISHER_NAME: str = None
    PUBLISHER_NAME_HREF: str = None
    RELEASE_NOTES_HREF: str = None
    DISPLAY_NAME: str = None
    ICON_HREF_DEFAULT: str = None
    ICON_HREF_HIGH_CONTRAST: str = None
    DESCRIPTION_HREF: str = None

    def __init__(self):

        if self.NAME is None:
            self.NAME = self.__class__.__name__

        if self.IDENTIFIER_BASE is None:
            self.IDENTIFIER_BASE = f'com.{self.AUTHOR.replace(" ", "_").lower()}.extensions'

        if self.IDENTIFIER is None:
            self.IDENTIFIER = f'{self.IDENTIFIER_BASE}.{self.NAME.replace(" ", "_").lower()}'

        if self.PUBLISHER_NAME is None:
            self.PUBLISHER_NAME = self.AUTHOR

        if self.DISPLAY_NAME is None:
            self.DISPLAY_NAME = self.NAME

        self.components: list[loxt_sidebar.SidebarModel] = list()

        # add components
        for attr in dir(self):
            if isinstance(getattr(self, attr), loxt_sidebar.SidebarModel):
                self.components.append(getattr(self, attr))
