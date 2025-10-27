from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    # First call DRF's default exception handler
    response = exception_handler(exc, context)

    if response is not None:
        response.data["status_code"] = response.status_code
        return response

    # For non-DRF exceptions (e.g. Python errors)
    return Response(
        {"error": str(exc), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
