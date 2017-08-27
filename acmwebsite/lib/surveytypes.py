class SurveyType:
    group_class = 'from-group'
    item_class = 'form-control'

    def __init__(self, name, on_first_time=False, **kwargs):
        self.params = kwargs
        self.name = name
        if on_first_time:
            self.group_class += ' on_first_time'

    def value(self, form):
        v = form.get(self.name)
        return v or None

    def parse(self, value):
        return value

    def html_params(self, **kwargs):
        params = {'class': self.item_class ,'name': self.name, **self.params, **kwargs}
        return ' '.join(['{}="{}"'.format(k, v) for k, v in params.items()])

    def dom(self):
        return '<input {} />'.format(self.html_params())

class Bool(SurveyType):
    group_class = 'checkbox'
    item_class = ''

    def __init__(self, checked=False, **kwargs):
        params = {'type': 'checkbox'}
        if checked:
            params['checked'] = 'checked'
        super().__init__(**params, **kwargs)

    def value(self, form):
        return 'true' if form.get(self.name) else 'false'

    def parse(self, value):
        return True if value == 'true' else False

class ShortText(SurveyType):
    def __init__(self, **kwargs):
        super().__init__(type='text', **kwargs)

class LongText(SurveyType):
    def __init__(self, value='', **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def dom(self):
        return '<textarea {}>{}</textarea>'.format(self.html_params(), self.value)

types = {k: v for k, v in globals().items() if isinstance(v, type) and issubclass(v, SurveyType)}