# -*- coding: utf-8 -*-

from authentic2.settings import INSTALLED_APPS, DATABASES,\
    TEMPLATE_DIRS

## AUTH_USER_MODEL = 'auth2_user.User'
INSTALLED_APPS = ['ldap_profile', ] + INSTALLED_APPS
TEMPLATE_DIRS = ('/usr/local/src/authentic2_novatus/ldap_profile/templates', )\
    + TEMPLATE_DIRS

AUTHENTICATION_BACKENDS = (
    'authentic2.backends.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LDAP_AUTH_SETTINGS = ({
    'url': ('ldap://agir.transfer-tic.org', ),
    'basedn': 'dc=transfer-tic,dc=org',
    'userdn': 'dc=transfer-tic,dc=org',
    'user_filter': 'sn=%s',
    'binddn': 'cn=admin,dc=transfer-tic,dc=org',
    'bindpw': 'transfer',
    'transient': False
    }, )


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
}

ROOT_URLCONF = 'urls'

DATABASES.update({'ldap': {
    'ENGINE': 'ldapdb.backends.ldap',
    'NAME': 'ldap://agir.transfer-tic.org/',
    'USER': 'cn=admin,dc=transfer-tic,dc=org',
    'PASSWORD': 'transfer', }, })

DATABASE_ROUTERS = ['ldapdb.router.Router']

CACHE_DIR = '/var/lib/authentic2/cache/'
