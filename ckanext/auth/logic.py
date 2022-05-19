import ckan.logic as logic
import ckan.lib.authenticator as authenticator
from ckan.common import _
from ckanext.emailasusername.blueprint import user_by_username_or_email

_check_access = logic.check_access


def user_login(context, data_dict):
    # Adapted from  https://github.com/ckan/ckan/blob/master/ckan/views/user.py#L203-L211
    generic_error_message = {
        u'errors': {
            u'auth': [_(u'Username or password entered was incorrect')]
        },
        u'error_summary': {_(u'auth'): _(u'Incorrect username or password')}
    }
    user = user_by_username_or_email(data_dict['id'], flash_errors=False)
    if not user:
        return generic_error_message

    user = user.as_dict()

    if data_dict[u'password']:
        identity = {
            u'login': user['name'],
            u'password': data_dict[u'password']
        }

        auth = authenticator.UsernamePasswordAuthenticator()
        authUser = auth.authenticate(context, identity)

        if authUser != user['name']:
            return generic_error_message
        else:
            return user
