from functools import wraps
from flask import jsonify, make_response, Response
from werkzeug.wrappers import Response as WerkzeugResponse


def format_response(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        response = func(*args, **kwargs)

        if isinstance(response, tuple):
            data, status_code = response
        else:
            data = response
            status_code = 200  # Default status code

        # If the response is an instance of Response or WerkzeugResponse, extract the JSON data
        if isinstance(data, (Response, WerkzeugResponse)):
            data = data.get_json()

        status_messages = {
            200: "OK",
            201: "Created",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
            700: "Wrong match in query",
        }

        status_message = status_messages.get(status_code, "Unknown Status")

        formatted_response = {
            "status": status_code,
            "state": status_message,
            "data": data,
        }

        return make_response(jsonify(formatted_response), status_code)

    return decorated_function
