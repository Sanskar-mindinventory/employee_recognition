# regex for Validation
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
USER_NAME_REGEX = r"^[A-Za-z\d@$!_#%*?&]{3,30}$"
VIDEO_MIME_TYPE_REGEX = r"^video\/(?:[^/]+\+)?(?:[a-z0-9\-]+)$"

# user
TEST_API_RESPONSE_DATA = {"success_msg": "This is secure data! To check whether System is working or not."}
MSG_RETRIEVE_USER = "Successfully retrieved user."
ERR_SQLALCHEMY_ERROR = "Error:{}"
MSG_USER_REGISTER_SUCCESSFULLY = "Hey {} you registered successfully."
MSG_LOG_IN_SUCCESSFULLY = "Successfully Logged in."
ERR_INVALID_USERNAME = "Please Enter Valid Username!"
ERR_INVALID_PASSWORD = "Please Enter Valid Password!"
ERR_USERNAME_EXISTS = "Username: {} is Already Exist!"
ERR_EMAIL_EXISTS = "Email: {} is Already Exist!"
ERR_INVALID_TOKEN = "Invalid Token"
SOMETHING_WENT_WRONG = "Oops! Something went wrong."
INVALID_CREDENTIALS = "Invalid credentials"
SUCCESS_EXECUTED = "Test API is working Fine. Current User : {user_name}"

# video upload
INVALID_FILE_TYPE = 'Uploaded file is invalid. Please upload valid video file only.'
VIDEO_UPLOADED_SUCCESSFULLY = "{video_name} is uploaded successfully."
FILTERED_DATA_SUCCESSFULLY = "Data is filtered as per the field {}"
