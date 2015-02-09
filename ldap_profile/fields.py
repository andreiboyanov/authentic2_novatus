from ldapdb.models.fields import ListField
from ldapdb import escape_ldap_filter
from django.utils.translation import ugettext as _
from django import forms
from widgets import ListWidget

class ListFormField(forms.CharField):
    message = _('Enter one item per line.')
    code = 'invalid'
    widget = ListWidget

    def to_python(self, value):
        if not value:
            return []
        return [v.strip() for v in value.splitlines() if v != ""]


class LdapListField(ListField):
    def formfield(self, **kwargs):
        defaults = {'form_class': ListFormField}
        defaults.update(kwargs)
        result = super(LdapListField, self).formfield(**defaults)
        return result

    def get_prep_lookup(self, lookup_type, value):
        "Perform preliminary non-db specific lookup checks and conversions"
        if lookup_type in ('contains', 'icontains'):
            return escape_ldap_filter(value)
        raise TypeError("ListField has invalid lookup: %s" % lookup_type)

