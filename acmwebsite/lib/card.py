from kajiki import FileLoader, XMLTemplate
from itertools import chain
from acmwebsite.lib import helpers

default_loader = FileLoader('acmwebsite/templates/cards')
default_loader.extension_map['xhtml'] = XMLTemplate

class CardTypes:
    """This class maintains a list of card generators. Any page that uses
    cards, should have a ``CardTypes`` instance in a global variable.
    """

    def __init__(self):
        self.list = []

    def register(
        self,
        generator,
        title_template=None,
        body_template=None,
        loader=default_loader,
    ):

        """
        """

        if title_template is not None:
            title_template = loader.load(f'{title_template}.xhtml')

        if body_template is not None:
            body_template = loader.load(f'{body_template}.xhtml')

        def _gen(*args, **kwargs):
            context = {
                "h": helpers,
            }

            for gened in generator(*args, **kwargs):
                if title_template is not None:
                    gened.title_escape = False
                    gened.title = title_template({
                        **context,
                        **gened.title,
                    }).render()

                if body_template is not None:
                    gened.body_escape = False
                    gened.body = body_template({
                        **context,
                        **gened.body,
                    }).render()

                yield gened

        self.list.append(_gen)

    def gen(self, *args, **kwargs):
        return chain(*(card_gen(*args, **kwargs) for card_gen in self.list))

class Card:
    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.title_escape = True
        self.body_escape = True
