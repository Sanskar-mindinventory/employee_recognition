from typing import Optional
from keycloak.keycloak_openid import KeycloakOpenID
from keycloak import KeycloakAdmin
from config.config import KeyCloakSettings



class KeyCloakUtils:
    """
    This is initial class of keycloak which contain connection of keycloak server connection
    and all other function of keycloak library.
    """
    def __init__(self) -> None:
        self.keycloak_openid = KeycloakOpenID(server_url=KeyCloakSettings().server_url, realm_name=KeyCloakSettings().realm_name, client_id=KeyCloakSettings().client_id, client_secret_key=KeyCloakSettings().secret_key)
        self.keycloak_admin = KeycloakAdmin(connection=self.keycloak_openid)

    def create_user(self, kwargs: dict):
        new_user = self.keycloak_admin.create_user(**kwargs)


