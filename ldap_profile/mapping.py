attribute_map = {
    'cn': {
        'display_name': 'displayName',
        'oid': '2.5.4.3',
        'profile_field_name': 'name',
        'syntax': '1.3.6.1.4.1.1466.115.121.1.15',
        'type': 'http://www.w3.org/2001/XMLSchema#string',
        'is_primary_key': True},
    'gn': {
        'alias': ['givenName'],
        'display_name': u'First name(gn givenName)',
        'namespaces': {
            'http://schemas.xmlsoap.org/ws/2005/05/identity/claims': {
                'friendly_names': ['First Name'],
                'identifiers': [
                    'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname']}},
                'oid': '2.5.4.42',
                'profile_field_name': 'first_name',
                'type': 'http://www.w3.org/2001/XMLSchema#string'},
    'mail': {
        'alias': ['rfc822Mailbox'],
        'display_name': 'mail rfc822Mailbox',
        'oid': '0.9.2342.19200300.100.1.3',
        'profile_field_name': 'email',
        'type': 'http://www.w3.org/2001/XMLSchema#string'},
    'o': {
        'alias': ['organizationName'],
        'display_name': u'Organization(o organizationName)',
        'oid': '2.5.4.10',
        'profile_field_name': 'company',
        'type': 'http://www.w3.org/2001/XMLSchema#string'},
    'postalAddress': {
        'display_name': u'Postal address(postalAddress)',
        'oid': '2.5.4.16',
        'profile_field_name': 'postal_address',
        'syntax': '1.3.6.1.4.1.1466.115.121.1.41',
        'type': 'http://www.w3.org/2001/XMLSchema#string'},
    'sn': {
        'alias': ['surname'],
        'display_name': u'Last name(sn surname)',
        'namespaces': {
            'http://schemas.xmlsoap.org/ws/2005/05/identity/claims': {
                'friendly_names': ['Last Name'],
                'identifiers': [
                    'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname']}},
        'oid': '2.5.4.4',
        'profile_field_name': 'username',
        'type': 'http://www.w3.org/2001/XMLSchema#string'},
    'telephoneNumber': {
        'display_name': u'Phone(telephoneNumber)',
        'namespaces': {
            'http://schemas.xmlsoap.org/ws/2005/05/identity/claims': {
                'friendly_names': ['Secondary or Work Telephone Number'],
                'identifiers': ['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/otherphone']}},
        'oid': '2.5.4.20',
        'profile_field_name': 'phone',
        'syntax': '1.3.6.1.4.1.1466.115.121.1.50{32}',
        'type': 'http://www.w3.org/2001/XMLSchema#string'},
    'description': {
        'display_name': 'description',
        'oid': '2.5.4.13',
        'profile_field_name': 'description',
        'syntax': '1.3.6.1.4.1.1466.115.121.1.15{1024}',
        'type': 'http://www.w4.org/2001/XMLSchema#string'},
    }
