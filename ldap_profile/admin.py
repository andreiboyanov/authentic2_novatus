from django.contrib import admin
from ldap_profile.models import ProfileAdmin, Profile

admin.site.register(Profile, ProfileAdmin)
