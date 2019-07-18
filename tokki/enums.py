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
            "errored": Status.Failed,  # Travis
            "canceled": Status.Canceled,  # Travis

            "cancelled": Status.Canceled,  # AppVeyor
            "cancelling": Status.Canceled,  # AppVeyor
            "queued": Status.InProgress,  # AppVeyor
            "running": Status.InProgress,  # AppVeyor
            "starting": Status.InProgress,  # AppVeyor
            "success": Status.InProgress,  # AppVeyor

            "failed": Status.Failed,  # Both
        }

        # If the name does not exists, throw an exception
        if name not in statuses:
            raise ValueError

        # Finally, return the value
        return statuses[name]
