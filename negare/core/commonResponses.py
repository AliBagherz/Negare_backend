from rest_framework import status
from rest_framework.response import Response

from .responseMessages import ErrorResponse


def successResponse(status_code=200, **kwargs):
    return Response(data={"success": True, **kwargs}, status=status_code)


def errorResponse(status_code=400, **kwargs):
    return Response(exception={"success": False, **kwargs}, status=status_code)


def invalidDataResponse():
    return errorResponse(status.HTTP_406_NOT_ACCEPTABLE, error=ErrorResponse.INVALID_DATA)
