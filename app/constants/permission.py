class Permission:
    """
    Constants for the various roles scoped in the application ecosystem
    """

    ADD_ADMIN = {
        "name": "ADD_ADMIN",
        "description": "Access for adding user to system",
        "persian_name": "افزودن مدیر"
    }
    UPDATE_ADMIN = {
        "name": "UPDATE_ADMIN",
        "description": "Access for updating admin",
        "persian_name": "بروزرسانی مدیر"
    }
    DELETE_ADMIN = {
        "name": "DELETE_ADMIN",
        "description": "Access for deleting admin",
        "persian_name": "حذف مدیر"
    }
    ADD_USER = {
        "name": "ADD_USER",
        "description": "Access for adding user",
        "persian_name": "افزودن کاربر"
    }
    ADD_RESUME_FOR_USERS = {
        "name": "ADD_RESUME",
        "description": "Access for adding user resume",
        "persian_name": "افزودن رزومه برای کاربران"
    }
    GET_USERS_RESUME_LIST = {
        "name": "GET_USERS_RESUME_LIST",
        "description": "Access to the list of users",
        "persian_name": "دیدن لیست کاربران"
    }

    GET_USER_RESUME = {
        "name": "GET_USER_RESUME",
        "description": "Access for get a user resume",
        "persian_name": "دیدن رزومه ی کاربران"
    }

    DELETE_USER = {
        "name": "DELETE_USER",
        "description": "Access for delete user",
        "persian_name": "حذف کاربران"
    }

    GET_ADMINS_LIST = {
        "name": "GET_ADMINS_LIST",
        "description": "Access for list of admins",
        "persian_name": "دیدن لیست مدیران"
    }

    permissions = [
        ADD_ADMIN,
        UPDATE_ADMIN,
        DELETE_ADMIN,
        ADD_USER,
        ADD_RESUME_FOR_USERS,
        GET_USERS_RESUME_LIST,
        GET_USER_RESUME,
        DELETE_USER,
        GET_ADMINS_LIST
    ]
