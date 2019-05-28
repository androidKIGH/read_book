from rest_framework.views import exception_handler
from .myresponse import JsonResponse
import logging

logger = logging.getLogger('error')


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.

    if isinstance(exc, MyError):
        logger.error(MyError.message)
        return JsonResponse(code=MyError.code, msg=MyError.message, data=MyError.data)

    response = exception_handler(exc, context)
    # #
    # # Now add the HTTP status code to the response.
    # if response is not None:
    #     response.status_code = 200

    return response


class MyError(Exception):
    data = None
    message = None
    code = None

    def __init__(self, code, message='failed', data=None):
        MyError.data = data
        MyError.message = message
        MyError.code = code
