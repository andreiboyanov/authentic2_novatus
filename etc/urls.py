# -*- coding: utf-8 -*-
from ldap_profile import urls as ldap_urls
from authentic2.urls import urlpatterns

urlpatterns += ldap_urls.urlpatterns
