class ErrorResponse:
    INVALID_DATA = "invalid data"
    NOT_FOUND = "item not found"
    DATETIME_A_DAY_ERROR = "your datetime should be in a single day"
    NOT_ENOUGH_DATA = "Not enough data"


class SuccessResponse:
    CREATED = "created!"
    DELETED = "deleted!"
    CHANGED = "changed!"
