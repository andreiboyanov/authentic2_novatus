from ldapdb.models.fields import CharField, ListField
from django.core.exceptions import FieldError
import ldapdb.models
from django.contrib import admin
from mapping import ATTRIBUTE_MAPPING as attribute_map

DEFAULT_FIELD_LENGTH = 200


def _get_field_len(field):
    try:
        return int(field['syntax'].split('{')[1].split('}')[0])
    except:
        return DEFAULT_FIELD_LENGTH


def get_profile(user):
    profile_object = Profile()
    user_name = user.username.split('@')[0]
    profiles = Profile.objects.filter(email__contains=user.email,
                                      username__contains=user_name)
    try:
        return profiles[0]
    except IndexError:
        return None


def get_ldap_fields():
    result = dict()
    for name, field in attribute_map.items():
	if not 'django_type' in field:
	    continue
        field_length = _get_field_len(field)
	if 'profile_field_name' not in field:
	    import pdb; pdb.set_trace()
        result.update({
            field.get('profile_field_name'):
            field['django_type'](db_column=name, max_length=field_length,
                                 blank=not field.get('is_required', False),
                                 unique=field.get('is_unique', False),
                                 primary_key=field.get('is_primary_key', False))})
    return result


class Meta:
    app_label = 'ldap_profile'

def get_attribute_aggregator_attributes(user, definitions=None, source=None,
				        auth_source=False, **kwargs):
    if not 'ldap' in source.name.lower():
        return None

    attribute_names = dict((name.lower(), name) for name in attribute_map.keys())
    ldap_attributes = dict()
    attributes = user.get_attributes()
    import pdb; pdb.set_trace()
    for attribute in attributes:
        if attribute in attribute_names:
	    ldap_attributes.update({attribute_names[attribute]:
		attributes[attribute]})
        else:
            ldap_attributes.update({attribute: 
		attributes[attribute]})

    data = [{'definition': attribute, 'values':
		isinstance(values, list) and values or [values]} for 
			attribute, values in ldap_attributes.iteritems()]
    return {source.name: data}

fields = get_ldap_fields()
fields.update({
    'object_classes': ['inetOrgPerson', 'organizationalPerson'],
    'Meta': Meta,
    '__module__': 'ldap_profile.models',
    '__str__': lambda self: self.name,
    '__unicode__': lambda self: self.name, })

fields.update({
    'base_dn': 'dc=transfer-tic,dc=org'})
Profile = type('Profile', (ldapdb.models.Model, ),
               fields.copy())


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email')
    search_fields = ('name', 'username', 'email')


from . import signals
