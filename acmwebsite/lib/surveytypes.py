from ast import literal_eval


class SurveyType:
    def __init__(self, name, label=None, required=False, first_time=False, **kwargs):
        self.name = name
        self.required = required
        self.first_time = first_time
        self.label = label

    def from_post(self, form):
        v = form.get(self.name)
        return repr(v or None)

    def from_contents(self, contents):
        return literal_eval(contents)


class Bool(SurveyType):
    template = 'checkbox'

    def __init__(self, value=None, **kwargs):
        super().__init__(**kwargs)
        self.checked = bool(value) and value != 'unchecked'

    def from_post(self, form):
        return str(bool(form.get(self.name)))


class Text(SurveyType):
    def __init__(self, value='', placeholder=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.placeholder = placeholder

    def from_post(self, form):
        v = form.get(self.name)
        return v or None

    def from_contents(self, contents):
        return contents


class ShortText(Text):
    template = 'text'


class LongText(Text):
    template = 'textarea'


class ManyOf(SurveyType):
    template = 'checkbox_group'

    def __init__(self, options='[]', **kwargs):
        super().__init__(**kwargs)
        self.options = literal_eval(options)

    def from_post(self, form):
        vals = [n for i, n in enumerate(self.options) if form.get('{}_{}'.format(self.name, i))]
        return str(vals)


class OneOf(SurveyType):
    template = 'radio_group'

    def __init__(self, options='[]', value=None, **kwargs):
        super().__init__(**kwargs)
        self.options = literal_eval(options)
        self.value = value

    def from_post(self, form):
        return form.get(self.name) or None

    def from_contents(self, contents):
        return contents


class Select(SurveyType):
    template = 'select'

    def __init__(self, options='[]', value=None, **kwargs):
        super().__init__(**kwargs)
        self.options = literal_eval(options)
        self.value = value
        self.multiple = False

    def from_post(self, form):
        return form.get(self.name) or None

    def from_contents(self, contents):
        return contents


class SelectMany(Select):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiple = True


class Number(SurveyType):
    template = 'number'

    def __init__(self, value=None, min=None, max=None, step=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.min = min,
        self.max = max,
        self.step = step

    def from_post(self, form):
        v = form.get(self.name)
        if v is None:
            return None
        return repr(float(v))


types = {
    k: v
    for k, v in globals().items()
    if isinstance(v, type) and issubclass(v, SurveyType)
}
