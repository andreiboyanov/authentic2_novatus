from django import forms
from models import get_profile_model


def LdapProfileForm(request):
    class LdapProfileFormClass(forms.ModelForm):
        error_css_class = 'form-field-error'
        required_css_class = 'form-field-required'

        class Meta:
            model = get_profile_model(request.user)

    return LdapProfileFormClass
