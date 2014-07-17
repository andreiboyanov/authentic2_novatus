# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from ldap_profile import views as ldap_views


urlpatterns = patterns(
    '',
    url(r'^profile/$', ldap_views.view_profile),
    url(r'^profile/change_password/$', ldap_views.change_password,
        name='ldap_change_password'),
    url(r'^profile/change_email/$', ldap_views.change_email,
        name='ldap_change_email'),
    url(r'^profile/edit/$', ldap_views.edit_profile,
        name='ldap_edit_profile'),
)
