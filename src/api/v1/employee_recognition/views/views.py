from typing import Annotated, List
from fastapi import APIRouter, Depends, Path, UploadFile
from src.api.v1.employee_recognition.schemas.employee_register_schemas import EmployeeRegister

from src.api.v1.employee_recognition.services.face_recognition_service import RecogEmployee
from src.api.v1.user_authentication.utils.auth_utils import active_user_is_admin

employee_router = APIRouter(
    prefix="/employee",
    dependencies=[Depends(active_user_is_admin)] 
)

@employee_router.get('/')
def get_employee_check():
    return {"Message" : "Employee Service is running perfectly."}, 200


@employee_router.post('/add')
def add_employee(employee: Annotated[EmployeeRegister, Depends()]):
    data=RecogEmployee().single_record_faces(file=employee.emp_image, empName=employee.emp_name)
    return {"msg":f"Successfully employee is added to the database with {employee.emp_name}"}, 201


@employee_router.delete('/delete/{emp_name}')
def delete_employee(emp_name: Annotated[str, Path(title='Provide Employee Name to delete Employee data')]):
    deleted_employee = RecogEmployee().delete_employee(employee_name=emp_name.lower())
    return {"msg": f"Deleted data of {emp_name}"}, 200


@employee_router.post('/add-multiple')
def add_multiple_employee(employee: List[UploadFile]):
    data=RecogEmployee().batch_record_faces(files=employee)
    return {"msg":f"Successfully employees are added."}, 201
