class InvalidRoleException(Exception):
    def __init__(self, message="Invalid user role"):
        super().__init__(message)

class InvalidCredentialsException(Exception):
    def __init__(self, message="Invalid credentials"):
        self.message = message
        super().__init__(self.message)

class MissingUserException(Exception):
    def __init__(self, message="Missing user with given id"):
        self.message = message
        super().__init__(self.message)
    
class AlreadySentFollowRequestException(Exception):
    def __init__(self, message="You've already sent follow request to that particular user"):
        self.message = message
        super().__init__(self.message)

class AlreadyFollowException(Exception):
    def __init__(self, message="You are already following that particular user"):
        self.message = message
        super().__init__(self.message)


class NotAuthorizedException(Exception):
    def __init__(self, message="You are not authorized to access this endpoint"):
        self.message = message
        super().__init__(self.message)

class TokenExpiredException(Exception):
    def __init__(self, message="JWT token has expired."):
        self.message = message
        super().__init__(self.message)

class InvalidDataException(Exception):
    def __init__(self, message="Invalid data"):
        super().__init__(message)

class InvalidAuthException(Exception):
    def __init__(self, message="Invalid auth data"):
        super().__init__(message)

class NotFoundException(Exception):
    def __init__(self, message="Entity not found"):
        super().__init__(message)

class NotAccessibleException(Exception):
    def __init__(self, message="Entity is private"):
        super().__init__(message)