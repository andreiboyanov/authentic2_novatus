# -*- coding: utf-8 -*-

from authentic2.settings import INSTALLED_APPS, DATABASES,\
    TEMPLATE_DIRS
## import mapping

## AUTH_USER_MODEL = 'auth2_user.User'
INSTALLED_APPS = ['ldap_profile', ] + INSTALLED_APPS
TEMPLATE_DIRS = ('/usr/local/src/authentic2_novatus/ldap_profile/templates', )\
   + TEMPLATE_DIRS

AUTHENTICATION_BACKENDS = (
    # 'authentic2.backends.LDAPBackend',
    'transferLDAPBackend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

import ldap
from django_auth_ldap.config import LDAPSearch

# Here put the LDAP URL of your server
AUTH_LDAP_SERVER_URI = 'ldap://localhost'

# Let the bind DN and bind password blank for anonymous binding
AUTH_LDAP_BIND_DN = "cn=admin,dc=transfer-tic,dc=org"
AUTH_LDAP_BIND_PASSWORD = "transfer"

# Lookup user under the branch o=base and by mathcing their uid against the
# received login name
AUTH_LDAP_USER_SEARCH = LDAPSearch("dc=transfer-tic,dc=org",
    ldap.SCOPE_SUBTREE, "(uid=%(user)s)")


ATTRIBUTE_MAPPING = 'mapping'

LDAP_AUTH_SETTINGS = ({
    'url': ('ldap://localhost', ),
    'basedn': 'dc=transfer-tic,dc=org',
    'email_field': 'mail',
    'fname_field': 'givenName',
    'lname_field': 'sn',
    'user_filter': 'uid=%s',
    'binddn': 'cn=admin,dc=transfer-tic,dc=org',
    'bindpw': 'transfer',
    'transient': False,
    'attribute_mappings': [],
    'attributes': ['cn', 'objectClass', 'photo', 'manager', 'title',
                   'facsimileTelephoneNumber', 'userCertificate',
                   'userPassword', 'preferredDeliveryMethod', 'mail',
                   'internationaliSDNNumber', 'postOfficeBox',
                   'departmentNumber', 'x500uniqueIdentifier', 'userPKCS12',
                   'employeeNumber', 'registeredAddress',
                   'physicalDeliveryOfficeName', 'roomNumber', 'l',
                   'x121Address', 'givenName', 'destinationIndicator',
                   'uid', 'seeAlso', 'jpegPhoto', 'entryUUID', 'street',
                   'description', 'employeeType', 'preferredLanguage',
                   'userSMIMECertificate', 'postalCode', 'postalAddress',
                   'homePostalAddress', 'pager', 'homePhone',
                   'telephoneNumber', 'audio', 'displayName',
                   'businessCategory', 'labeledURI', 'mobile',
                   'teletexTerminalIdentifier', 'o', 'st', 'carLicense',
                   'sn', 'telexNumber', 'ou', 'secretary', 'initials'],
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
   'NAME': 'ldap://localhost/',
   'USER': 'cn=admin,dc=transfer-tic,dc=org',
   'PASSWORD': 'transfer', }, })

DATABASE_ROUTERS = ['ldapdb.router.Router']

CACHE_DIR = '/var/lib/authentic2/cache/'
A2_HOMEPAGE_URL = '/profile/'
