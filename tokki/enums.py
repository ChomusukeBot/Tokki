from enum import Enum


class Status(Enum):
    """
    Represents the status of a CI build.
    """
    InProgress = 0
    Success = 1
    Failed = 2
