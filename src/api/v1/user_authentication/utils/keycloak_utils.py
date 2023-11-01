from typing import Optional
from keycloak.keycloak_openid import KeycloakOpenID
from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection
from config.config import 





class KeyCloakUtils:
    """
    This is initial class of keycloak which contain connection of keycloak server connection
    and all other function of keycloak library.
    """
    def __init__(self) -> None:
        self.keycloak_openid = KeycloakOpenID(server_url=server_url, realm_name=realm_name, client_id=client_id, client_secret_key=secret_key)
        self.keycloak_admin = KeycloakAdmin(connection=self.keycloak_openid)

    def create_user(self, kwargs: dict):
        new_user = self.keycloak_admin.create_user(**kwargs)



