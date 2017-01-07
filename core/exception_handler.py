import logging

from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.compat import set_rollback
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    # to get the standard error response.
    response = exception_handler(exc, context)

    # response == None is an exception not handled by the DRF framework in the call above
    if response is None:
        logger.error(exc)
        response = Response({'detail': 'Unhandled server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        set_rollback()

    # TODO: log this

    return response
