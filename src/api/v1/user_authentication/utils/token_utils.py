from jose import jwt
from config.config import JWTSettings
from datetime import datetime, timedelta


class Token:
    def __init__(self):
        self.secret_key = JWTSettings().authjwt_secret_key
        self.algorithm = JWTSettings().JWT_ALGORITHM
        self.expiry_time = JWTSettings().ACCESS_TOKEN_EXPIRE_TIME_MINUTES

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.expiry_time)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
