"""
Contains custom errors and exceptions for Nephos
"""


class DBException(Exception):
    """
    Handles exceptions concerning Database
    """
    def __init__(self, message):
        super().__init__(message)
