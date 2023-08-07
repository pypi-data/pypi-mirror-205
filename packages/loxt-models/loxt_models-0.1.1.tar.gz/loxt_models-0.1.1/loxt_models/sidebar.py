from loxt_models import deck as loxt_deck


class SidebarModel:

    def __init__(self):
        self.decks: list[loxt_deck.DeckModel] = list()

        # add decks
        for attr in dir(self):
            if isinstance(getattr(self, attr), loxt_deck.DeckModel):
                self.decks.append(getattr(self, attr))
