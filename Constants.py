from enum import Enum


class Prefix(Enum):
    ALLOWED = ['*']
    RESTRICTED = ['prod']


class StatusCodes(Enum):
    SUCCESS_STATUS_CODE = 200
    ERROR_STATUS_CODE = 500


class ServiceState(Enum):
    RUNNING = "Running"
    PENDING = "Pending"
    CHECKING = "Checking"
    SERVICE_NOT_FOUND = "Service not found"


class Operations(Enum):
    GET_STATUS = "status"
    UPDATE_SERVICE = "update"


