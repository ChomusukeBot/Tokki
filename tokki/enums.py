from enum import Enum


class Status(Enum):
    """
    Represents the status of a CI build.
    """
    InProgress = 0
    Success = 1
    Failed = 2
    Canceled = 3

    @staticmethod
    def from_name(name):
        """
        Returns the correct Status from the string outputed of a CI service.
        """
        # A dict with the correct statuses
        statuses = {
            "created": Status.InProgress,  # Travis
            "received": Status.InProgress,  # Travis
            "started": Status.InProgress,  # Travis
            "passed": Status.Success,  # Travis
            "failed": Status.Failed,  # Travis
            "errored": Status.Failed,  # Travis
            "canceled": Status.Canceled,  # Travis

            "success": Status.Success,  # AppVeyor
        }

        # If the name does not exists, throw an exception
        if name not in statuses:
            raise ValueError

        # Finally, return the value
        return statuses[name]