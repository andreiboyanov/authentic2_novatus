import ldapdb.models
from django.contrib import admin
from mapping import ATTRIBUTE_MAPPING as attribute_map
from fields_order import fields_order

DEFAULT_FIELD_LENGTH = 200


def get_attribute_aggregator_attributes(user, definitions=None, source=None,
                                        auth_source=False, **kwargs):
    if 'ldap' not in source.name.lower():
        return None

    attribute_names = dict((name.lower(), name) for name in
                           attribute_map.keys())
    ldap_attributes = dict()
    attributes = user.get_attributes()
    for attribute in attributes:
        if attribute in attribute_names:
            ldap_attributes.update({attribute_names[attribute]:
                                   attributes[attribute]})
        else:
            ldap_attributes.update({attribute:
                                   attributes[attribute]})
    ldap_attributes.update({'uid': [user.username.split('@')[0]]})

    data = [{'definition': attribute, 'values':
             isinstance(values, list) and values or [values]} for
            attribute, values in ldap_attributes.iteritems()]
    return {source.name: data}


def _get_field_len(field):
    try:
        return int(field['syntax'].split('{')[1].split('}')[0])
    except:
        return DEFAULT_FIELD_LENGTH


def get_profile(user):
    user_name = user.username.split('@')[0]
    profiles = Profile.objects.filter(email__contains=user.email,
                                      username__contains=user_name)
    try:
        return profiles[0]
    except IndexError:
        return None


def get_ldap_fields():
    result = dict()
    #FIXME: Get fields from settings.LDAP_AUTH_SETTINGS['attributes'] ??
    for name in fields_order:
        field = attribute_map[name]
        if 'django_type' not in field:
            continue
        field_length = _get_field_len(field)
        result.update({
            field.get('profile_field_name', name):
            field['django_type'](db_column=name, max_length=field_length,
                                 blank=not field.get('is_required', False),
                                 editable=not field.get('hidden', False),
                                 unique=field.get('is_unique', False),
                                 primary_key=field.get('is_primary_key',
                                                       False))})
    return result


class Meta:
    app_label = 'ldap_profile'


fields = get_ldap_fields()
fields.update({
    'object_classes': ['inetOrgPerson', 'organizationalPerson'],
    'Meta': Meta,
    '__module__': 'ldap_profile.models',
    '__str__': lambda self: self.name,
    '__unicode__': lambda self: self.name, })

fields.update({
    'base_dn': 'ou=People,dc=transfer-tic,dc=org'})
Profile = type('Profile', (ldapdb.models.Model, ),
               fields.copy())


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('repr_first_name', 'repr_last_name',
                    'repr_username', 'repr_email')
    # list_display_links = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'username', 'email')

    def repr_list(self, value):
        return ', '.join(value)

    def repr_first_name(self, user):
        return self.repr_list(user.first_name)

    def repr_last_name(self, user):
        return self.repr_list(user.last_name)

    def repr_username(self, user):
        return self.repr_list(user.username)

    def repr_email(self, user):
        return self.repr_list(user.email)


from signals import init_signals
init_signals()
