from django.contrib import admin
from ldap_profile.models import ProfileAdmin,\
    ProfileFormateur, ProfileParticipant, ProfileEncadrant

admin.site.register(ProfileEncadrant, ProfileAdmin)
admin.site.register(ProfileParticipant, ProfileAdmin)
admin.site.register(ProfileFormateur, ProfileAdmin)
