from flask import Blueprint, jsonify, make_response, request

from auth.decorators import token_required
from auth.models import app_group

bp = Blueprint("app_group", __name__)


@bp.route("/app_group", methods=["POST"])
@token_required
def create_group(current_user):
    """Create authorization relationship between User and App_Group.

    Parameters
    ----------
    group_name : `str`
        Name of the Group to be created.
    secured_app_id : `str`
        ID for the App to be related to the Group.

    Returns
    -------
    response : <Response [201 CREATED]>
    {
        "group_name": group_name,
        "id": id
    }
    """
    data = request.json
    group_id = app_group.add(
        data["group_name"], data["secured_app_id"], current_user
    )
    return make_response(
        jsonify({"id": group_id, "group_name": data["group_name"]}),
        201,
    )


@bp.route("/app_groups", methods=["GET"])
@token_required
def get_all(current_user):
    """Fetch all App Groups from the Database.

    Returns
    -------
    response : <Response [200 OK]>
    {
        "app_groups": [
            {
                "app_name": app_name,
                "created_by": created_by,
                "id": id
            }
        ],
        "current_user": current_user
    }
    """
    return make_response(
        jsonify(
            {"app_groups": app_group.get_all(), "current_user": current_user}
        ),
        200,
    )
