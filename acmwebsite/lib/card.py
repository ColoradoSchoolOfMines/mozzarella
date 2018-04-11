# -*- coding: utf-8 -*-
from kajiki import FileLoader, XMLTemplate
from itertools import chain
from acmwebsite.lib import helpers


default_loader = FileLoader('acmwebsite/templates/cards')
default_loader.extension_map['xhtml'] = XMLTemplate


class CardTypes:
    """Maintains a list of card generators. Any page can use cards by instantiating
    a :class:`CardTypes` variable.
    """

    def __init__(self):
        self.list = []

    def register(self, generator, title_template=None, body_template=None, loader=default_loader):
        """Register a new card generator

        :param generator: a generator function that yields individual cards.
        :param title_template: (optional) the file where the Kajiki template
            for the cards' title is. Defaults to ``None``.
        :param body_template: (optional) the file where the Kajiki template
            for the cards' body is. Defaults to ``None``.
        :param loader: (optional) a Kahjiki :class:`FileLoader` object that is
            used to load the aforementioned template files. Defaults to a
            :class:`FileLoader` object in the 'acmwebsite/templates/cards'
            directory
        :return: ``None``
        :rtype: None
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
        """Generates an iterable that contains all of the cards

        All arguments passed to this function are immediately passed to the
        registered (see :func:`register`) generators. The return value of this
        function can be passed to the `section` function defined in
        acmwebsite/templates/card_section.xhtml, whose return value can in turn
        be used to generate the cards in any location on a webpage.

        For example, a webpage's Kajiki file can generate cards by first
        importing the card api::
            <py:import href="acmwebsite.templates.card_section" alias="cards"/>

        and then, when necessary, generating the cards anywhere on the webpage::
            ${cards.section(cardlist)}
        """
        return chain(*(card_gen(*args, **kwargs) for card_gen in self.list))


class Card:
    """A data structure which defines the basic elements of a card. Objects of this
    type are stored in a :class:`CardTypes` object, and should be returned by
    registered generator functions.
    """
    def __init__(self, title, body):
        """Create a :class:`Card` with a given title and body.

        :param title: the title of the card; this will be displayed in the
            header.
        :param body: the body of the card; this will be displayed in the main
            section of the card.
        """
        self.title = title
        self.body = body
        self.title_escape = True
        self.body_escape = True
