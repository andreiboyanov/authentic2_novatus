# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_noop
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlencode

from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.auth.hashers import check_password, make_password


import ldap
from ldap.filter import filter_format
import authentic2.backends
from django_auth_ldap.backend import populate_user
from authentic2.compat import get_user_model

from authentic2.backends.ldap_backend import LDAPUser
from base64 import b64decode
from binascii import unhexlify, hexlify
from md5 import md5
import hashlib

User = get_user_model()

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
        md5_password = md5(password).hexdigest()
	return ldap_password == md5_password

    # Taken from http://www.openldap.org/faq/data/cache/347.html
    def check_sha1_password(self, ldap_password, password):
        digest = ldap_password[:20]
        salt = ldap_password[20:]
        hashed_password = hashlib.sha1(password)
        hashed_password.update(salt)
        return digest == hashed_password.digest()

    def make_user(self, ldap_record):
	user = User(username=ldap_record[1]['uid'][0])
	return user

    # inspired by the AUFLDAPBackend class from http://git.auf.org/?p=authentic2.git
    def authenticate(self, username, password):
        """
        Try to find the ldap user with the given username and password.
	Firstable, retrieve all users with the given username. 
	Second, find this one having the right password.
	Remeber that our user records may contain several uids, passwords and emails
        """
	try:
            conn = ldap.initialize('ldap://localhost')
            conn.simple_bind('cn=admin,dc=transfer-tic,dc=org', 'transfer')
            user_basedn = 'dc=transfer-tic,dc=org'
            query = '(uid={user})'.format(user=username)
            results = conn.search_s(user_basedn, ldap.SCOPE_SUBTREE, query)
            for result in results:
                for ldap_password in result[1]['userPassword']:
		    if self.check_password(ldap_password, password):
                        user = self.make_user(result)
                        return user 
        except ldap.NO_SUCH_OBJECT:
            log.error('user bind failed: unable to lookup user '
                    'basedn {} not found'.format(user_basedn))
        except ldap.LDAPError, e:
            log.error('user bind failed: unable to lookup user {}: {}: '
                      ''.format(username, e))
        return None

    def authenticate_block(self, block, username, password):
        """
        Rewrite of the original authentic2.LDAPBackend.authenticate() method
        I need everything it does except the len(results) > 1 check
        If len(results) > 1 then we try to bind with every one of the users
        in the results list
        """
        for opt in ('NETWORK_TIMEOUT', 'TIMELIMIT', 'TIMEOUT'):
            ldap.set_option(getattr(ldap, 'OPT_%s' % opt), block['timeout'])
        utf8_username = username.encode('utf-8')
        utf8_password = password.encode('utf-8')

        for uri in block['url']:
            log.debug('try to bind user on %r', uri)
            conn = ldap.initialize(uri)
            authz_id = None
            user_basedn = block.get('user_basedn', block['basedn'])

            try:
                # if necessary bind as admin
                self.try_admin_bind(conn, block)
                if block['user_dn_template']:
                    authz_id = block['user_dn_template'].format(username=username)
                else:
                    try:
                        if block.get('bind_with_username'):
                            authz_id = utf8_username
                        elif block['user_filter']:
                            try:
                                query = filter_format(block['user_filter'], (utf8_username,))
                            except TypeError, e:
                                log.error('user_filter syntax error %r: %s',
                                        block['user_filter'], e)
                                return
                            log.debug('looking up dn for username %r using '
                                    'query %r', username, query)
                            results = conn.search_s(user_basedn, ldap.SCOPE_SUBTREE, query)
                            if len(results) == 0:
                                log.debug('user bind failed: not entry found')
                            elif len(results) > 1:
                                log.warning('too many (%d) entries found', len(results))
                                authz_id = [results[i][0] for i in range(len(results))]
                            else:
                                authz_id = [results[0][0],]
                        else:
                            raise NotImplementedError
                    except ldap.NO_SUCH_OBJECT:
                        log.error('user bind failed: unable to lookup user '
                                'basedn %s not found', user_basedn)
                        if block['replicas']:
                            break
                        continue
                    except ldap.LDAPError, e:
                        log.error('user bind failed: unable to lookup user %r: '
                                '%s', username, e)
                        continue
                if authz_id is None:
                    continue
                authenticated_user = None
                try:
                    for id in authz_id:
                        try:
                            conn.simple_bind_s(id, utf8_password)
                            authenticated_user = id
                            break
                        except ldap.INVALID_CREDENTIALS:
                            log.debug('user bind failed: invalid credentials with %s', uri)
                            # if block['replicas']: # FIXME: reproduce this logic
                            #    break              # in the new ´multiuser´ algorithm
                            # continue
                except ldap.LDAPError, e:
                    log.error('Got error from LDAP library: %s' % str(e))
                    return None
                if authenticated_user is not None:
                    user = self._return_user(uri, authenticated_user, username, password, conn, block)
                    return user;
            except ldap.SERVER_DOWN:
                log.error('ldap authentication error: %r is down', uri)
            finally:
                del conn
        return None
