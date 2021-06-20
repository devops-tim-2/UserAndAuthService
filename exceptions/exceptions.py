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