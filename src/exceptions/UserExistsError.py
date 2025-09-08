class UserExistsError(Exception):
    """
        If the user with same email exists in DB, UserExistsError occurur.

        Args:
            message(str): explanation of the error
    """
    def __init__(self, message="An user with same email exists!"):
        super().__init__(message)
