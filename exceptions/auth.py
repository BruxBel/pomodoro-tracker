class TokenExpiredException(Exception):
    detail = "Token expired"


class TokenNotCorrectException(Exception):
    detail = "Token not correct"
