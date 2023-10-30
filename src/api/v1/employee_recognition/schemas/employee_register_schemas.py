from ast import List
from typing_extensions import Annotated
from click import File
from fastapi import Form, UploadFile

from src.api.v1.employee_recognition.validations.employee_validations import Validation

class FormValidation:
    def __new__(cls, *args, **kwargs):
        cls.validate_object(*args, **kwargs)
        instance = super().__new__(cls)
        return instance

    @classmethod
    def validate_object(cls, *args, **kwargs):
        pass


class EmployeeRegister(FormValidation):
    def __init__(self, emp_name:Annotated[str, Form()], emp_image:Annotated[UploadFile, File()]) -> None:
        self.emp_name = emp_name.lower()
        self.emp_image= emp_image

    @classmethod
    def validate_object(cls, *args, **kwargs):
        if kwargs.get('emp_name'):
            return Validation().name_validation(name=kwargs.get('emp_name'))
        



# from fastapi import File, Form, UploadFile
# from typing_extensions import Annotated

# class UserProfileForm:
#     def init(self, profile_img: Annotated[UploadFile, File()], first_name: Annotated[str, Form(...)], last_name: Annotated[str, Form(...)], email: Annotated[str, Form(...)], phone_number: Annotated[str, Form(...)], address: Annotated[str, Form(...)], password: Annotated[str, Form(...)], role: Annotated[str, Form(...)],):
#         self.profile_img = profile_img
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         self.phone_number = phone_number
#         self.address = address
#         self.password = password
#         self.role = role```