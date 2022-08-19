from flask import Blueprint, jsonify, make_response, request

from auth.decorators import token_required
from auth.models import authorization

bp = Blueprint("authorization", __name__)


@bp.route("/authorization", methods=["POST"])
@token_required
def create_authorization(current_user):
    data = request.json
    payload = authorization.add(
        data["user_id"], data["group_id"], current_user
    )
    return make_response(jsonify(payload), 201)


@bp.route("/authorizations", methods=["GET"])
@token_required
def get_all(current_user):
    return make_response(
        jsonify(
            {
                "authorizations": authorization.get_all(),
                "current_user": current_user,
            }
        ),
        200,
    )
