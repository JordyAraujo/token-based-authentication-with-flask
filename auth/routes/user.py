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


@bp.route("/signup", methods=["POST"])
def create_user():
    data = request.json
    payload = {"username": data["username"]}
    token = jwt.encode(payload, app.config.SECRET_KEY, "HS256").decode("utf-8")
    user.add(data["username"], token)
    return make_response(jsonify({"token": token}), 201)
