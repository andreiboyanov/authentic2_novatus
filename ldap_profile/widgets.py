import six
from django.forms.widgets import Textarea
from django.core.exceptions import ValidationError
from django.core import validators

LIST_FIELD_EMPTY_VALUES = validators.EMPTY_VALUES + ('[]', )


class ListWidget(Textarea):
    is_hidden = False

    def prep_value(self, value):
        if value in LIST_FIELD_EMPTY_VALUES:
            return ""
        elif isinstance(value, six.string_types):
            return value
        elif isinstance(value, list):
            return "\n".join(value)
        raise ValidationError('Invalid format.')

    def render(self, name, value, attrs=None):
        value = self.prep_value(value)
        if attrs is None:
            attrs = dict()
        if 'rows' not in attrs:
            attrs.update({'rows': 3})
        return super(ListWidget, self).render(name, value, attrs)
