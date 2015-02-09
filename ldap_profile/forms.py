from models import Profile
import django
from mapping import ATTRIBUTE_MAPPING as attribute_map


def LdapProfileForm(request):
    class LdapProfileFormClass(django.forms.ModelForm):
        error_css_class = 'form-field-error'
        required_css_class = 'form-field-required'

        def __init__(self, *args, **kwargs):
            super(LdapProfileFormClass, self).__init__(*args, **kwargs)
            for name, field in attribute_map.iteritems():
                field_name = field.get('profile_field_name', name)
                if field_name in self.fields:
                    self.fields[field_name].label = \
                        field.get('display_name', field)

        class Meta:
            model = Profile
            widgets = {
                'dn': django.forms.TextInput(attrs={'readonly': 'readonly'}),
            }
            # NOTE: The following wouldn't work with Django < 1.6
            labels = dict([(field['profile_field_name'], field['display_name'])
                          for name, field in attribute_map.iteritems()
                          if 'profile_field_name' in field])

    return LdapProfileFormClass
