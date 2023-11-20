from fastapi import status
import keycloak
from src.api.v1.user_authentication.utils.auth_utils import verify_user_details_for_access

from src.api.v1.user_authentication.utils.hash_utils import Hasher
from src.api.v1.user_authentication.utils.keycloak_utils import KeyCloakUtils
from src.api.v1.user_authentication.utils.token_utils import Token
from src.api.v1.user_authentication.models.user_models import User
from src.api.v1.user_authentication.utils.constants import ERR_USERNAME_EXISTS, ERR_EMAIL_EXISTS, ERR_SQLALCHEMY_ERROR, MSG_USER_LOGIN_SUCCESSFUL, \
    MSG_USER_REGISTER_SUCCESSFULLY, ERR_INVALID_USERNAME, ERR_INVALID_PASSWORD, MSG_LOG_IN_SUCCESSFULLY, \
    ERR_INVALID_TOKEN, MSG_RETRIEVE_USER, INVALID_CREDENTIALS, TEST_API_RESPONSE_DATA, SUCCESS_EXECUTED, USER_DATA_UPDATED_SUCCESSFULLY
from src.utils.response_utils import Response


class UserServices:

    @staticmethod
    def register(request, db_session):
        """
        This function is used for registration of user.
        :param request: request body
        :param db_session: Database Session
        :return: registered User.
        """
        user_name = request.user_name
        email = request.email
        if User.get_user_by_email(db_session, email):
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message=ERR_EMAIL_EXISTS.format(email)).send_error_response()
        if User.get_user_by_username(db_session, user_name):
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message=ERR_USERNAME_EXISTS.format(user_name)).send_error_response()
        keycloak_user_id = KeyCloakUtils().create_user(kwargs=request.dict())
        user_data = request.dict()
        user_data['keycloak_id'] = keycloak_user_id
        is_saved, data_or_error = User.save(db_session,user_data)
        if is_saved is False:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message=ERR_SQLALCHEMY_ERROR.format(data_or_error)).send_error_response()
        return Response(status_code=status.HTTP_201_CREATED,
                        message=MSG_USER_REGISTER_SUCCESSFULLY.format(user_name), data=data_or_error). \
            send_success_response()

    @staticmethod
    def login(request, db_session):
        """
        This function is used by the login API.
        :param request: request body
        :param db_session: Database Session
        :return: access token and type of token
        """
        stored_user = User.get_user_by_username(db_session, request.user_name)
        if stored_user is None or not Hasher.verify_password(request.password, stored_user.password):
            raise Response(status_code=status.HTTP_401_UNAUTHORIZED, message=INVALID_CREDENTIALS).send_error_response()
        access_token = Token().create_access_token(
            data={"sub": stored_user.user_name})
        return Response(status_code=status.HTTP_200_OK, message=MSG_USER_LOGIN_SUCCESSFUL,data={"access_token": access_token, "token_type": "bearer"}).send_success_response()

    @staticmethod
    def get_token(form_data, db_session):
        """
        This function is used by the Authorize button of the OpenAPI doc.
        :param form_data: Authentication Form
        :param db_session: Database Session
        :return: access token and type of token
        """
        stored_user = User.get_user_by_username(db_session, form_data.username)
        if stored_user is None or not Hasher.verify_password(form_data.password, stored_user.password):
            raise Response(status_code=status.HTTP_401_UNAUTHORIZED, message=INVALID_CREDENTIALS).send_error_response()
        access_token = Token().create_access_token(
            data={"sub": stored_user.user_name}
        )
        return {"access_token": access_token, "token_type": 'bearer'}

    @staticmethod
    def test_api(current_user):
        """
        This is a testing function
        :param current_user: Current User
        :return: response for testing API
        """
        return Response(status_code=status.HTTP_200_OK,
                        message=SUCCESS_EXECUTED.format(user_name=current_user.user_name),
                        data=TEST_API_RESPONSE_DATA)


    @staticmethod
    def update_user(user_id,request, db_session, current_user):        
        current_logged_in_user = verify_user_details_for_access(current_user=current_user, user_id=user_id)
        user = User.get_user_by_user_id(user_id=user_id, db_session=db_session)
        keycloak_user = KeyCloakUtils().update_user(user_id=user.keycloak_id, kwargs=request.dict(exclude_unset=True))
        user_update = User.update_user_by_user_id(db_session=db_session, update_kwargs=request.dict(exclude_unset=True), user_id=user_id)
        return Response(status_code=status.HTTP_200_OK,message=USER_DATA_UPDATED_SUCCESSFULLY).send_success_response()