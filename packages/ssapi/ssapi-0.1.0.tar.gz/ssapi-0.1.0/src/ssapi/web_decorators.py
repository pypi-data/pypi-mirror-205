import json
from functools import wraps

from bottle import request, response

from ssapi.defaults import DEFAULT_SSAPI_WEB_CONTENT_TYPE
from ssapi.web_tools import camel_to_snake_case


def accepts_json(callable):
    @wraps(callable)
    def wrapper(*args, **kwargs):
        if request.headers["content-type"] == DEFAULT_SSAPI_WEB_CONTENT_TYPE:
            try:
                request.adapted_json = camel_to_snake_case(request.json)
            except json.JSONDecodeError as exc:
                response.status = 400
                return {
                    "outcome": f"error: invalid JSON: {request.body}: {exc}"
                }

        return callable(*args, **kwargs)

    return wrapper


def returns_json(callable):
    @wraps(callable)
    def wrapper(*args, **kwargs):
        response.content_type = DEFAULT_SSAPI_WEB_CONTENT_TYPE
        return json.dumps(callable(*args, **kwargs))

    return wrapper
