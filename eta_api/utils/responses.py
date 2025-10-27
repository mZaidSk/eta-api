# utils/responses.py
from rest_framework.response import Response


def success_response(data=None, message="Request successful", status=200, meta=None):
    """
    Standard success response.
    :param data: The payload data (dict, list, or object).
    :param message: Human-readable success message.
    :param status: HTTP status code.
    :param meta: Optional metadata (e.g., pagination).
    """
    response = {
        "success": True,
        "message": message,
        "data": data,
        "errors": None,
    }

    if meta is not None:
        response["meta"] = meta

    return Response(response, status=status)


def error_response(errors=None, message="Something went wrong", status=400, data=None):
    """
    Standard error response.
    :param errors: Dict or list of error details.
    :param message: Human-readable error message.
    :param status: HTTP status code.
    :param data: Optional data (in case you want to return partial results).
    """
    return Response(
        {
            "success": False,
            "message": message,
            "data": data,
            "errors": errors or {},
        },
        status=status,
    )
