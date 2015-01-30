from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.edit import UpdateView
from django.shortcuts import render_to_response
from authentic2.decorators import prevent_access_to_transient_users
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

import forms
from models import get_profile, Profile


@prevent_access_to_transient_users
def view_profile(request):
    try:
        profile = get_profile(request.user)
        if profile is None:
            return HttpResponseRedirect("/logout/")
        profile_list = [(field.name, [getattr(profile, field.name), ])
                        for field in profile._meta.fields]
        return render_to_response('ldap_profile.html',
                                  {'profile': profile_list, },
                                  RequestContext(request))
    except (ObjectDoesNotExist):
        return HttpResponseRedirect("/logout/")
    except (MultipleObjectsReturned):
        return HttpResponseRedirect("/profile/ldap_error")



@prevent_access_to_transient_users
def change_password(request):
    pass


@prevent_access_to_transient_users
def change_email(request):
    pass


class EditProfile(UpdateView):
    template_name = 'edit_ldap_profile.html'
    success_url = '../'

    def get_object(self):
        self.model = Profile
        self.form_class = forms.LdapProfileForm(self.request)
        return get_profile(self.request.user)


edit_profile = prevent_access_to_transient_users(EditProfile.as_view())

# End
