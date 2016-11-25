from rest_framework.exceptions import APIException


class StripeCardError(APIException):

    original_error = {}

    def __init__(self, err):
        self.detail = err.json_body["error"]["message"]
        self.code = err.json_body["error"]["code"]
        self.status_code = err.http_status
        self.original_error = err.json_body


class StripePaymentError(APIException):

    original_error = {}

    def __init__(self, err):
        self.status_code = err.http_status
        self.detail = str(err)
        self.original_error = err.json_body
