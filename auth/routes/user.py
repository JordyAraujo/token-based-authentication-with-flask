import jwt
from flask import Blueprint
from flask import current_app as app
from flask import jsonify, make_response, request

from auth.decorators import token_required
from auth.models import user

bp = Blueprint("user", __name__)


@bp.route("/users", methods=["GET"])
@token_required
def get_all(current_user):
    """Fetch all users from the Database.

    Returns
    -------
    response : <Response [200 OK]>
    {
        "current_user": current_user,
        "users": [
            {
                "id": id,
                "token": token,
                "username": username
            }
        ]
    }
    """
    return make_response(
        jsonify({"users": user.get_all(), "current_user": current_user}), 200
    )


@bp.route("/login", methods=["GET"])
def login():
    """Authenticate user credentials.

    Parameters
    ----------
    token : `str`
        Token to be authenticated.

    OR

    username : `str`
        Username to be authenticated.
    password : `str`
        Password to be authenticated.

    Returns
    -------
    response : <Response [200 OK]>
    {
        "token": token
    }

    OR

    response : <Response [401 OK]>
    {
        "token": null
    }
    """
    response_token = None
    token_data = None
    if "token" in request.json:
        given_token = request.json["token"]
        response_token = (
            given_token if user.token_exists(given_token) else None
        )
    else:
        given_token = jwt.encode(
            {
                "username": request.json["username"],
                "password": request.json["password"],
            },
            app.config.SECRET_KEY,
            "HS256",
        )
        token_data = user.get_token(request.json["username"])
        if token_data:
            response_token = (
                token_data["token"]
                if given_token == token_data["token"]
                else None
            )

    return make_response(
        jsonify({"token": response_token}), 200 if response_token else 401
    )


@bp.route("/signup", methods=["POST"])
def create_user():
    """Create user credentials.

    Parameters
    ----------
    username : `str`
        Username for the user to be created.
    password : `str`
        Password for the user to be created.

    Returns
    -------
    response : <Response [201 CREATED]>
    {
        "token": token
    }
    """
    token = user.add(request.json)
    return make_response(jsonify({"token": token}), 201)
