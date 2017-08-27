class SurveyType:
    group_class = 'from-group'
    item_class = 'form-control'

    def __init__(self, on_first_time=False, **kwargs):
        self.params = kwargs
        if 'name' in kwargs.keys():
            self.name = kwargs['name']
        if on_first_time:
            self.group_class += ' on_first_time'

    def value(self, form):
        v = form.get(self.name)
        return v or None

    def parse(self, value):
        return value

    def html_params(self, **kwargs):
        params = {'class': self.item_class, **self.params, **kwargs}
        return ' '.join(['{}="{}"'.format(k, v) for k, v in params.items()])

    def dom(self):
        return '<input {} />'.format(self.html_params())

class SelectionComponent(SurveyType):
    """
    Superclass for Radio and Checkbox types, both of these are
    "selection components with labels".

    Not to be used alone as a Survey Type in the database.
    """

    def __init__(self, checked=False, disabled=False, **kwargs):
        params = {}
        if checked:
            params['checked'] = 'checked'
        if disabled:
            params['disabled'] = 'disabled'
        super().__init__(**params, **kwargs)

    def parse(self, value):
        return True if value == 'true' else False

class Checkbox(SelectionComponent):
    group_class = 'checkbox'
    item_class = ''

    def __init__(self, **kwargs):
        super().__init__(type='checkbox', **kwargs)

    def value(self, form):
        return 'true' if form.get(self.name) else 'false'

class Radio(SelectionComponent):
    """
    Radio Component (not a group!). Radios are a bit funky in HTML and
    this implementation is not exempt from the funkyness. In short:

    1. The radio GROUP is the 'name' parameter. This is HTML's fault.
    2. The value the radio stores is the 'value' parameter.

    For elogence, I think this should eventually be wrapped in a
    "RadioGroup" component that abstracts away HTML's funkyness, not
    quite too sure what's a good way to approach this tho.
    """

    group_class = 'radio'
    item_class = ''

    def __init__(self, value, **kwargs):
        self.val = value
        super().__init__(type='radio', value=value, **kwargs)

    def value(self, form):
        return 'true' if form.get(self.name, None) == self.val else 'false'

class ShortText(SurveyType):
    def __init__(self, **kwargs):
        super().__init__(type='text', **kwargs)

class LongText(SurveyType):
    def __init__(self, value='', **kwargs):
        super().__init__(**kwargs)
        self.val = value

    def dom(self):
        return '<textarea {}>{}</textarea>'.format(self.html_params(), self.val)

class GroupComponent(SurveyType):
    """
    Superclass for all components which have multiple components.
    Not to be used directly.
    """

    def __init__(self, subfields, **kwargs):
        self.subfields = subfields
        super().__init__(**kwargs)

    def dom(self):
        """
        YOU must recursively generate the DOM of group components.
        (as it's your responsibility to handle labels etc.)
        """
        raise NotImplementedError

class Section(GroupComponent):
    """
    A section of fields
    """
    group_class = 'section'

class SelectionGroup(GroupComponent):
    """
    A group of radio options or checkboxes
    """
    group_class = 'selection-group'


types = {k: v for k, v in globals().items() if isinstance(v, type) and issubclass(v, SurveyType)}