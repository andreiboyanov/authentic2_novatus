from django import forms
from models import Profile


def LdapProfileForm(request):
    class LdapProfileFormClass(forms.ModelForm):
        error_css_class = 'form-field-error'
        required_css_class = 'form-field-required'

        class Meta:
            model = Profile

    return LdapProfileFormClass
