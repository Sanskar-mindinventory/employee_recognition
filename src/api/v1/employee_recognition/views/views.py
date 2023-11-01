from typing import Annotated, List
from fastapi import APIRouter, Depends, Path, UploadFile, status
from src.api.v1.employee_recognition.schemas.employee_register_schemas import EmployeeRegister

from src.api.v1.employee_recognition.services.face_recognition_service import RecogEmployee
from src.api.v1.employee_recognition.utils.constants import EMPLOYEE_ADDED_SUCCESSFULLY, EMPLOYEE_DELETED_SUCCESSFULLY, MULTIPLE_EMPLOYEES_ARE_ADDED
from src.api.v1.user_authentication.utils.auth_utils import active_user_is_admin
from src.utils.response_utils import Response

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
    return Response(status_code=status.HTTP_201_CREATED,
                        message=EMPLOYEE_ADDED_SUCCESSFULLY.fomrat(employee.emp_name)). \
            send_success_response()


@employee_router.delete('/delete/{emp_name}')
def delete_employee(emp_name: Annotated[str, Path(title='Provide Employee Name to delete Employee data')]):
    deleted_employee = RecogEmployee().delete_employee(employee_name=emp_name.lower())
    return Response(status_code=status.HTTP_200_OK,
                    message=EMPLOYEE_DELETED_SUCCESSFULLY.fomrat(emp_name)). \
        send_success_response()


@employee_router.post('/add-multiple')
def add_multiple_employee(employee: List[UploadFile]):
    data=RecogEmployee().batch_record_faces(files=employee)
    return Response(status_code=status.HTTP_201_CREATED,
                        message=MULTIPLE_EMPLOYEES_ARE_ADDED). \
        send_success_response()


