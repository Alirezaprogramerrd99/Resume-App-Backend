class Error:
    """
    Constants for the errors
    """
    USER_EXIST_ERROR = {
        "text": "کاربری با این ایمیل در سیستم موجود است.",
        "code": 409
    }
    PERMISSION_DENIED_ERROR = {
        "text": "خطای دسترسی",
        "code": 401
    }
    USER_NOT_FOUND = {
        "text": "کاربری با این ایمیل در سیستم وجود ندارد.",
        "code": 404
    }
    CODE_EXPIRATION_OR_NOT_EXIST_ERROR = {
        "text": "کد اشتباه است یا منقضی شده است.",
        "code": 404
    }
    USER_PASS_WRONG_ERROR = {
        "text": "نام کاربری یا رمز عبور اشتباه است.",
        "code" : 401
    }
    TOKEN_NOT_EXIST_OR_EXPIRATION_ERROR = {
        "text": "توکن منقضی شده است یا وجود ندارد.",
        "code" : 403
    }
    INACTIVE_USER = {
        "text" : "کاربر غیر فعال است.",
        "code" : 400
    }
