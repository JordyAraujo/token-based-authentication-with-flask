from functools import wraps

import jwt
from flask import current_app as app
from flask import jsonify, make_response, request


def token_required(secured_function):
    """Requires token authentication before executing decorated function."""

    @wraps(secured_function)
    def decorator(*args, **kwargs):
        token = None
        # ensure the jwt-token is passed with the headers
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:  # throw error if no token provided
            return make_response(
                jsonify({"message": "A valid token is missing!"}), 401
            )
        try:
            data = jwt.decode(
                str(token), app.config.SECRET_KEY, algorithms=["HS256"]
            )
            current_user = data["username"]
        except Exception:
            return make_response(jsonify({"message": "Invalid token!"}), 401)
            # Return the user information attached to the token
        return secured_function(current_user, *args, **kwargs)

    return decorator
