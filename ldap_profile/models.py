from ldapdb.models.fields import CharField
from django.core.exceptions import FieldError
import ldapdb.models
from django.contrib import admin
from . import mapping

DEFAULT_FIELD_LENGTH = 200


def _get_field_len(field):
    try:
        return int(field['syntax'].split('{')[1].split('}')[0])
    except:
        return DEFAULT_FIELD_LENGTH


# FIXME: Do it with a single LDAP call instead of 2 as actually
# (but how??)
def get_profile_model(user):
    user_name = user.username.split('@')[0]
    import pdb; pdb.set_trace()
    profile = Profile.objects.filter(email=user.email, username=user_name)[0]
    profile_types = {
        'ou=formateur': ProfileFormateur,
        'ou=encadrant': ProfileEncadrant,
        'ou=participant': ProfileParticipant,
        }

    profile_object = None
    for profile_type in profile_types:
        if profile_type in profile.dn:
            profile_object = profile_types[profile_type]
            break
    if profile_object is None:
        raise(FieldError('Unknown profile type {}. Must be in {}'.
                         format(profile_types.keys())))
    return profile_object


def get_profile(user):
    profile_object = Profile()
    user_name = user.username.split('@')[0]
    profiles = Profile.objects.filter(email=user.email,
		                     username=user_name)
    try:
        return profiles[0]
    except IndexError:
        return None

    ##'email': CharField(db_column='mail', max_length=200, unique=False),
    ##'name': CharField(db_column='cn', max_length=200, primary_key=True),
    ##'username': CharField(db_column='sn', max_length=200, unique=False),


def get_ldap_fields():
    result = dict()
    for name, field in mapping.attribute_map.items():
        field_length = _get_field_len(field)
        result.update({
            field['profile_field_name']:
            CharField(db_column=name, max_length=field_length,
                      blank=not field.get('is_required', False),
                      unique=field.get('is_unique', False),
                      primary_key=field.get('is_primary_key', False))})
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
    'base_dn': 'dc=transfer-tic,dc=org'})
Profile = type('Profile', (ldapdb.models.Model, ),
               fields.copy())

## fields.update({
##     'base_dn': 'ou=formateur,ou=Usersdev,dc=transfer-tic,dc=org'})
## ProfileFormateur = type('ProfileFormateur', (ldapdb.models.Model, ),
##                         fields.copy())
## 
## fields.update({
##     'base_dn': 'ou=participant,ou=users,dc=transfer-tic,dc=org'})
## ProfileParticipant = type('ProfileParticipant', (ldapdb.models.Model, ),
##                           fields.copy())
## 
## fields.update({
##     'base_dn': 'ou=encadrant,ou=users,dc=transfer-tic,dc=org'})
## ProfileEncadrant = type('ProfileEncadrant', (ldapdb.models.Model, ),
##                         fields.copy())
## 

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email')
    search_fields = ('name', 'username', 'email')
