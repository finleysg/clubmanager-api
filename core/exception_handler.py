import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.compat import set_rollback
from rest_framework.response import Response
from raven.contrib.django.raven_compat.models import client

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    # to get the standard error response.
    response = exception_handler(exc, context)

    client.captureException(exc)

    # response == None is an exception not handled by the DRF framework in the call above
    if response is None:
        logger.error(exc)

        if isinstance(exc, IntegrityError):
            response = Response({"detail": "Must be unique - that one is already being used"}, status=status.HTTP_409_CONFLICT)
        else:
            response = Response({'detail': 'Unhandled server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        set_rollback()

    return response
