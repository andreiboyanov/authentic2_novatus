# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView

from authentic2 import urls

urlpatterns = patterns(
    '',
    (r'login/$', 'aufcustom.auth2_auth.views.login'),
    (r'password/change/$', 'aufcustom.auth2_auth.views.password_change'),
    url(r'^a-propos$', TemplateView.as_view(template_name="a-propos.html"),
        name="a-propos"),
    (r'^politique-de-mot-de-passe$', TemplateView.as_view(
        template_name="politique-de-mot-de-passe.html")),
    url(r'^reinitialisation-du-mot-de-passe$',
        'aufcustom.views.reinitialisation_du_mot_de_passe',
        name='reinitialisation_du_mot_de_passe'),
) + urls.urlpatterns
