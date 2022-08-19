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
    return make_response(
        jsonify({"users": user.get_all(), "current_user": current_user}), 200
    )


@bp.route("/login", methods=["GET"])
def login():
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
    payload = request.json
    token = jwt.encode(payload, app.config.SECRET_KEY, "HS256")
    user.add(payload["username"], token)
    return make_response(jsonify({"token": token}), 201)
