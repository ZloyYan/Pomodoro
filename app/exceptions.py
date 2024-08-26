class UserNotFoundException(Exception):
    detail = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail = "Incorrect password"

class TokenExpiredException(Exception):
    detail = "Token expired"

class InvalidTokenException(Exception):
    detail = "Invalid token"



class TaskNotFoundException(Exception):
    detail = "Task not found"