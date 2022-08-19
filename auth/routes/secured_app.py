import jwt
from flask import Blueprint
from flask import current_app as app
from flask import jsonify, make_response, request

from auth.decorators import token_required
from auth.models import secured_app

bp = Blueprint("secured_app", __name__)


@bp.route("/secured_apps", methods=["GET"])
@token_required
def get_all(current_user):
    return make_response(
        jsonify(
            {
                "secured_apps": secured_app.get_all(),
                "current_user": current_user,
            }
        ),
        200,
    )


@bp.route("/secured_app", methods=["POST"])
@token_required
def create_app(current_user):
    data = request.json
    payload = {"app_name": data["app_name"]}
    secret_key = jwt.encode(payload, app.config.SECRET_KEY, "HS256")
    app_id = secured_app.add(data["app_name"], secret_key)
    return make_response(
        jsonify(
            {
                "id": app_id,
                "current_user": current_user,
                "app_name": data["app_name"],
                "secret_key": secret_key,
            }
        ),
        201,
    )
