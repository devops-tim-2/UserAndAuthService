class InvalidRoleException(Exception):
    def __init__(self, message="Invalid user role"):
        super().__init__(message)

class InvalidCredentialsException(Exception):
    def __init__(self, message="Invalid credentials"):
        self.message = message
        super().__init__(self.message)