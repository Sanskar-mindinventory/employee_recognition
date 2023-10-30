from typing import Optional, Union
from pydantic_extra_types.country import CountryAlpha2, CountryAlpha3
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from enum import Enum as PyEnum
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
