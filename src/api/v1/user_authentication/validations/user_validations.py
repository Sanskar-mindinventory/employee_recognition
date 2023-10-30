from src.api.v1.user_authentication.utils.constants import USER_NAME_REGEX, ERR_INVALID_USERNAME, PASSWORD_REGEX, \
    ERR_INVALID_PASSWORD
from src.api.v1.user_authentication.validations.regex_validations import RegexValidation


def username_validation(username=None):
    """
    This method validate the username
    :param username: username
    :return: username if True else raise exception
    """
    return RegexValidation(username, USER_NAME_REGEX, ERR_INVALID_USERNAME).regex_validator()


def password_validation(password=None):
    """
    This method validate the password
    :param password: password
    :return: password if True else raise exception
    """
    return RegexValidation(password, PASSWORD_REGEX, ERR_INVALID_PASSWORD).regex_validator()
