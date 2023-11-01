from pydantic_settings import BaseSettings

from src.utils.aws_utils import SecretManagerUtils

class PathSettings:
    train_folder_path: str ='images/train'
    test_folder_path: str ='images/test'
    delete_folder_path: str ='images/delete'

class Settings(BaseSettings):
    DEBUG: bool = True
    TESTING: bool = False


class JWTSettings:
    jwt_secrets = SecretManagerUtils.get_secret(secret_name='employee-recognition-JWT-secret', region_name='us-east-2')
    ACCESS_TOKEN_EXPIRE_TIME_MINUTES: int = jwt_secrets.get('ACCESS_TOKEN_EXPIRE_TIME_MINUTES')
    REFRESH_TOKEN_EXPIRE_TIME_HOURS: int = jwt_secrets.get('REFRESH_TOKEN_EXPIRE_TIME_HOURS')
    JWT_ALGORITHM: str = jwt_secrets.get('JWT_ALGORITHM')
    AUTH_JWT_HEADER_TYPE: str = jwt_secrets.get('AUTH_JWT_HEADER_TYPE')
    AUTH_SECRET_KEY: str = jwt_secrets.get('AUTH_SECRET_KEY')
    AUTH_JWT_DECODE_ALGORITHMS: list = jwt_secrets.get('AUTH_JWT_DECODE_ALGORITHMS')
    authjwt_secret_key: str = jwt_secrets.get('authjwt_secret_key')


class DatabaseSettings:
    db_secrets = SecretManagerUtils.get_secret(secret_name='employee-recognition-db', region_name='us-east-1')
    DATABASE_USERNAME: str = db_secrets.get('DATABASE_USERNAME')
    DATABASE_PASSWORD: str = db_secrets.get('DATABASE_PASSWORD')
    DATABASE_HOST: str = db_secrets.get('DATABASE_HOST')
    DATABASE_NAME: str = db_secrets.get('DATABASE_NAME')
    DATABASE_PORT: int = db_secrets.get('DATABASE_PORT')


class DatabaseURLSettings(DatabaseSettings):
    SQLALCHEMY_DATABASE_URL: str = f"postgresql+psycopg2://{DatabaseSettings().DATABASE_USERNAME}:{DatabaseSettings().DATABASE_PASSWORD}@{DatabaseSettings().DATABASE_HOST}:{DatabaseSettings().DATABASE_PORT}/{DatabaseSettings().DATABASE_NAME}"


class KeyCloakSettings:
    keycloak_secret = SecretManagerUtils.get_secret(secret_name='employee-recognition-keycloak-secrets', region_name='us-east-1')
    KEYCLOAK_SERVER_URL: str = keycloak_secret.get('KEYCLOAK_SERVER_URL')
    REALM_NAME: str = keycloak_secret.get('REALM_NAME')
    CLIENT_ID: str = keycloak_secret.get('CLIENT_ID')
    SECRET_KEY: str = keycloak_secret.get('SECRET_KEY')