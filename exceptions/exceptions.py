class InvalidRoleException(Exception):
    def __init__(self, message="Invalid user role"):
        super().__init__(message)
