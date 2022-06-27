""" Module that stores custom exception(s).
"""

class InvalidRSSException(BaseException):
    """ Exception that can be raised when the given url is not valid RSS url or cannot be parsed
    """
    def __init__(self, *args, **krargs):
        """ Constructor of InvalidRSSException class
        """
        self.error_message = "The provided url is not a valid RSS url"