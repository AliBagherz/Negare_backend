from rest_framework import status
from rest_framework.response import Response

from .responseMessages import ErrorResponse


def invalidDataResponse():
    return Response(
        exception={
            "error": ErrorResponse.INVALID_DATA,
        },
        status=status.HTTP_406_NOT_ACCEPTABLE,
    )
