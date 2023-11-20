from datetime import datetime
from pickle import TRUE
from typing import Any

from sqlalchemy import String, Column, DateTime, Integer, Boolean, Enum, Text, ForeignKey
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import relationship

from database.database import Base
from src.api.v1.user_authentication.schemas.user_schemas import RoleChoices
from src.api.v1.user_authentication.utils.hash_utils import Hasher
from src.utils.custom_exception import KeyCloakUserCreationError


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, unique=True)
    user_name = Column(String(30), nullable=False, unique=True)
    password = Column(String(), nullable=False)
    email = Column(String(320), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now())
    is_admin_access = Column(Boolean, default=False, nullable=False)
    disabled = Column(Boolean, default=False, nullable=False)
    role = Column(Enum(RoleChoices), default=RoleChoices.Employee, nullable=False)
    first_name = Column(String(length=20))
    last_name = Column(String(length=20))
    phone_number = Column(String(length=20))
    keycloak_id = Column(String(), nullable=False)


    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.user_name = kwargs.get("user_name")
        self.email = kwargs.get("email")
        self.password = Hasher.hash_password(kwargs.get("password"))
        self.role = kwargs.get('role')
        self.keycloak_id = kwargs.get('keycloak_id')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.phone_number = kwargs.get('phone_number')

        if self.keycloak_id is None:
            raise KeyCloakUserCreationError("It might be possible that user is not created successfully in KeyCloak.")

    @classmethod
    def save(cls, db_session, data):
        try:
            address = data.pop('address')
            user = cls(**data)
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            address['user_id'] = user.user_id
            Address.save(db_session=db_session, data=address)
            return True, user
        except IntegrityError as e:
            error = e.orig.diag.message_detail[4:].split("=")
            return False, error[0] + error[1]
        except SQLAlchemyError as e:
            return False, e.__str__()

    @classmethod
    def get_user_by_email(cls, db_session: Any, email: str):
        return db_session.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_user_by_username(cls, db_session: Any, user_name: str):
        return db_session.query(cls).filter(cls.user_name == user_name).first()

    @classmethod
    def get_user_by_user_id(cls, db_session: Any, user_id: int):
        return db_session.query(cls).filter(cls.user_id == user_id).first()
    
    @classmethod
    def update_user_by_user_id(cls, db_session:Any, user_id:int, update_kwargs):
        db_session.query(cls).filter(cls.user_id == user_id).update(update_kwargs)
        db_session.commit()
        return True

    def __repr__(self) -> str:
        return f"<User {self.user_id}>"


class Address(Base):
    __tablename__ = 'Address'
    address_id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    line1 = Column(Text, nullable=False)
    line2 = Column(Text, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)

    # relationships
    user = relationship("User", backref='addresses')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.line1 = kwargs.get('line1')
        self.line2 = kwargs.get('line2')
        self.city = kwargs.get('city')
        self.state = kwargs.get('state')
        self.country = kwargs.get('country')
        self.user_id = kwargs.get('user_id')

    @classmethod
    def save(cls, db_session, data):
        try:
            address = cls(**data)
            db_session.add(address)
            db_session.commit()
            db_session.refresh(address)
            return True, address
        except IntegrityError as e:
            error = e.orig.diag.message_detail[4:].split("=")
            return False, error[0] + error[1]
        except SQLAlchemyError as e:
            return False, e.__str__()

    # @classmethod
    # def get_user_by_email(cls, db_session: Any, email: str):
    #     return db_session.query(cls).filter(cls.email == email).first()

    # @classmethod
    # def get_user_by_username(cls, db_session: Any, user_name: str):
    #     return db_session.query(cls).filter(cls.user_name == user_name).first()

    # @classmethod
    # def get_user_by_user_id(cls, db_session: Any, user_id: int):
    #     return db_session.query(cls).filter(cls.user_id == user_id).first()

    def __repr__(self) -> str:
        return f"<Address {self.address_id}>"
