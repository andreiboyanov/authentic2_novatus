# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_noop
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlencode

from django.contrib.auth import login, REDIRECT_FIELD_NAME


import ldap
from ldap.filter import filter_format
import authentic2.backends
from django_auth_ldap.backend import populate_user
from authentic2.compat import get_user_model

from authentic2.backends.ldap_backend import LDAPUser as AuthenticLDAPUser
from base64 import b64decode
from binascii import unhexlify, hexlify
import hashlib

EMPTY_PASSWORD = '!'

# FIXME - don't we need a custom logger here?
from django_auth_ldap.config import _LDAPConfig
log = _LDAPConfig.get_logger()


class LDAPBackend(authentic2.backends.LDAPBackend):
    """
    Custom backend for LDAP authentication made to authenticate users 
    with possibly multiple uids, userPasswords and mails in the LDAP record.
    Connects with binddn and bindpw, retrieves the user corresponding to the
    configured ldap filter. Than tries consecutively to match the given password
    with every password in the record
    """

    def backend_name(self):
        return '{}.{}'.format(__name__, self.__class__.__name__)

    def check_password(self, ldap_password, password):
        if ldap_password.lower().startswith('{ssha}'):
	    return self.check_sha1_password(ldap_password[6:],
					    password)
        elif ldap_password.lower().startswith('{md5}'):
	    return self.check_md5_password(
			    hexlify(b64decode(ldap_password[5:])),
			    password)
        else:
	    return self.check_md5_password(ldap_password,
                                           password)

    def check_md5_password(self, ldap_password, password):
        md5_password = hashlib.md5(password).hexdigest()
	return ldap_password == md5_password

    # Taken from http://www.openldap.org/faq/data/cache/347.html
    def check_sha1_password(self, ldap_password, password):
        digest = ldap_password[:20]
        salt = ldap_password[20:]
        hashed_password = hashlib.sha1(password)
        hashed_password.update(salt)
        return digest == hashed_password.digest()

    def map_attribtues(self, config, ldap_attributes):
	mapping = dict(config['attribute_mappings'])
	result = dict()
	for attribute, values in ldap_attributes.iteritems():
	    if attribute in mapping.keys():
                attribute = mapping[attribute]
            result.update({attribute: values})
        return result

    def authenticate_block(self, config, username, password):
        """
        Try to find the ldap user with the given username and password.
	Firstable, retrieve all users with the given username. 
	Second, find this one having the right password.
	Remeber that our user records may contain several uids, passwords and emails
        """
	try:
	    url = config['url'][0]
            connection = ldap.initialize(url)
            connection.simple_bind(config['binddn'], config['bindpw'])
            user_basedn = config['basedn']
            query = '(uid={user})'.format(user=username)
            results = connection.search_s(user_basedn, ldap.SCOPE_SUBTREE, query)
            for result in results:
                for ldap_password in result[1]['userPassword']:
		    if self.check_password(ldap_password, password):
			dn = result[0]
			attributes = self.map_attribtues(config, result[1])
        		user = self._return_user(url, dn, username, password,
						 connection, config)
                        return user 
        except ldap.NO_SUCH_OBJECT:
            log.error('user bind failed: unable to lookup user '
                    'basedn {} not found'.format(user_basedn))
        except ldap.LDAPError, e:
            log.error('user bind failed: unable to lookup user {}: {}: '
                      ''.format(username, e))
        return None
