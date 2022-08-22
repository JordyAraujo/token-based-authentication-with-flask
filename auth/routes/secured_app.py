from flask import Blueprint, jsonify, make_response, request

from auth.decorators import token_required
from auth.models import secured_app

bp = Blueprint("secured_app", __name__)


@bp.route("/secured_apps", methods=["GET"])
@token_required
def get_all(current_user):
    """Fetch all Secured Apps from the Database.

    Returns
    -------
    response : <Response [200 OK]>
    {
        "current_user": current_user,
        "secured_apps": [
            {
                "app_name": app_name,
                "created_by": created_by,
                "id": id
            }
        ]
    }
    """
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
    """Authenticate user credentials.

    Parameters
    ----------
    app_name : `str`
        Name for the App to be Secured.

    Returns
    -------
    response : <Response [201 CREATED]>
    {
        "app_name": app_name,
        "id": id
    }
    """
    data = request.json
    app_id = secured_app.add(data["app_name"], current_user)
    secured_app.by_name(data["app_name"])
    secured_app.by_id(app_id)
    return make_response(
        jsonify({"id": app_id, "app_name": data["app_name"]}),
        201,
    )
