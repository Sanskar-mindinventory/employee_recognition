from typing import Optional
from keycloak.keycloak_openid import KeycloakOpenID
from keycloak import KeycloakAdmin, KeycloakOpenIDConnection
from config import credentials
from config.config import KeyCloakSettings



class KeyCloakUtils:
    """
    This is initial class of keycloak which contain connection of keycloak server connection
    and all other function of keycloak library.
    """
    def __init__(self) -> None:
        self.keycloak_credentials = KeyCloakSettings()
        self.keycloak_openid = KeycloakOpenID(server_url=self.keycloak_credentials.KEYCLOAK_SERVER_URL, user_realm_name=self.keycloak_credentials.REALM_NAME,realm_name=self.keycloak_credentials.REALM_NAME, client_id=self.keycloak_credentials.CLIENT_ID, client_secret_key=self.keycloak_credentials.SECRET_KEY, verify=True)
        self.keycloak_admin = KeycloakAdmin(connection=self.keycloak_openid)

    def create_user(self, kwargs: dict):
        user_kwargs = {
                "username": kwargs.get('user_name'),
                "email": kwargs.get('email'),
                "firstName": kwargs.get("first_name"),
                "lastName": kwargs.get('last_name'),
                "enabled": True,
                "emailVerified": True,
                "credentials":[{
                    "value": kwargs.get("password"),
                    "type": "password"
                }],
                "attributes":{"phone_number":kwargs.get("phone_number"),"address": kwargs.get('address', 'N/A')}
            }
        new_user_id = self.keycloak_admin.create_user(user_kwargs)
        return new_user_id


    def update_user(self, user_id, kwargs):
        data = {'attributes':{}}
        if kwargs.get('first_name'):
              data['firstName'] = kwargs.get('first_name')
        if kwargs.get('last_name'):
            data['lastName'] = kwargs.get('last_name')
        if kwargs.get('phone_number'):
            data['attributes']['phone_number'] = kwargs.get('phone_number')
        keycloak_update = self.keycloak_admin.update_user(user_id=user_id, payload=data)
        return keycloak_update
    

    def logout_user(self, refresh_token):
        self.keycloak_openid.logout(refresh_token)