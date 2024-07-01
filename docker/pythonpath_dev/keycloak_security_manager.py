from flask_appbuilder.security.manager import AUTH_OID
from superset.security import SupersetSecurityManager
from flask_oidc import OpenIDConnect
from flask_appbuilder.security.views import AuthOIDView
from flask_login import login_user
from urllib.parse import quote
from flask_appbuilder.views import expose
from flask import request, redirect

import logging

class CustomSsoSecurityManager(SupersetSecurityManager):

    def oauth_user_info(self, provider, response=None):
        logging.debug("Oauth2 provider: {0}.".format(provider))
        if provider == 'keycloak':
            # res = self.appbuilder.sm.oauth_remotes[provider].get('userinfo')
            # logging.info(f"userinfo response:{res}")
            me=response['userinfo']
            logging.debug("user_data: {0}".format(me))
        return { 'name' : me['given_name'], 'email' : me['email'], 'id' : me['sid'], 'username' : me['preferred_username'], 'first_name':me['given_name'], 'last_name':me['family_name']}
    # def auth_user_oauth(self, userinfo):
    #     user = super(CustomSsoSecurityManager, self).auth_user_oauth(userinfo)
    #     roles = [self.find_role(x) for x in userinfo['roles']]
    #     roles = [x for x in roles if x is not None]
    #     user.roles = roles
    #     logging.debug(' Update <User: %s> role to %s', user.username, roles)
    #     self.update_user(user)  # update user roles
    #     return user 

class OIDCSecurityManager(SupersetSecurityManager):

    def __init__(self, appbuilder):
        super(OIDCSecurityManager, self).__init__(appbuilder)
        if self.auth_type == AUTH_OID:
            self.oid = OpenIDConnect(self.appbuilder.get_app)
        self.authoidview = AuthOIDCView


class AuthOIDCView(AuthOIDView):

    @expose('/login/', methods=['GET', 'POST'])
    def login(self, flag=True):
        sm = self.appbuilder.sm
        oidc = sm.oid
        superset_roles = ["Admin", "Alpha", "Gamma", "Public", "granter", "sql_lab"]
        default_role = "Public"

        @self.appbuilder.sm.oid.require_login
        def handle_login():
            user = sm.auth_user_oid(oidc.user_getfield('email'))

            if user is None:
                info = oidc.user_getinfo(['preferred_username', 'given_name', 'family_name', 'email', 'roles'])
                roles = [role for role in superset_roles if role in info.get('roles', [])]
                roles += [default_role, ] if not roles else []
                user = sm.add_user(info.get('preferred_username'), info.get('given_name', ''), info.get('family_name', ''),
                info.get('email'), [sm.find_role(role) for role in roles])
                login_user(user, remember=False)
            return redirect(self.appbuilder.get_url_for_index)

        return handle_login()

    @expose('/logout/', methods=['GET', 'POST'])
    def logout(self):
        oidc = self.appbuilder.sm.oid

        oidc.logout()
        super(AuthOIDCView, self).logout()
        redirect_url = request.url_root.strip('/')
        # redirect_url = request.url_root.strip('/') + self.appbuilder.get_url_for_login

        return redirect(
            oidc.client_secrets.get('issuer') + '/protocol/openid-connect/logout?redirect_uri=' + quote(redirect_url)) + '&id_token_hint=' + oidc.get_id_token()
