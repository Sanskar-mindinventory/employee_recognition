from typing import Optional, Union
from fastapi import Depends
from pydantic_extra_types.country import CountryAlpha2, CountryAlpha3
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from enum import Enum as PyEnum
from database.database import get_db
from src.api.v1.user_authentication.validations.user_validations import password_validation, username_validation


class RoleChoices(PyEnum):
    SuperAdmin = 'SuperAdmin'
    Admin = 'Admin'
    Employee = 'Employee'
    HOD = 'Head of Department'


class AddressSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    line1: str
    line2: Optional[str] = None
    city: str
    state: str
    country: Union[CountryAlpha3, CountryAlpha2]


class UserRegistrationRequestSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    user_name: str
    password: str
    email: EmailStr
    first_name: str = ''
    last_name: str = ''
    phone_number: str = ''
    role: RoleChoices
    address: AddressSchema

    # validators
    @field_validator('user_name')
    def username_validation_option(cls, value):
        return username_validation(username=value)

    @field_validator('password')
    def password_validation_option(cls, value):
        return password_validation(password=value)


class UserLoginRequestSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    user_name: str
    password: str

    # validators
    @field_validator('user_name')
    def username_validation_option(cls, value):
        return username_validation(username=value)


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    user_name: str
    email: str
    role: RoleChoices
    address: AddressSchema

class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = None 
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

class AddressUpdateSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[Union[CountryAlpha3, CountryAlpha2]]