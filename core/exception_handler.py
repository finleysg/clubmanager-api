from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.compat import set_rollback
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    # to get the standard error response.
    response = exception_handler(exc, context)

    # response == None is an exception not handled by the DRF framework in the call above
    if response is not None:
        response.data['status_code'] = response.status_code
    # else:
    #     response = Response({'detail': 'Unhandled server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     response.data['status_code'] = 500
    #
    #     set_rollback()

    return response
