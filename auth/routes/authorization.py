from flask import Blueprint, jsonify, make_response, request

from auth.decorators import token_required
from auth.models import authorization

bp = Blueprint("authorization", __name__)


@bp.route("/authorization", methods=["POST"])
@token_required
def create_authorization(current_user):
    """Create authorization relationship between User and App_Group.

    Parameters
    ----------
    user_id : `str`
        ID of the User to be authorized.
    group_id : `str`
        ID for the Group to be addedto the User.

    Returns
    -------
    response : <Response [201 CREATED]>
    {
        "app_group": app_group,
        "app_name": app_name,
        "username": username
    }
    """
    data = request.json
    payload = authorization.add(
        data["user_id"], data["group_id"], current_user
    )
    return make_response(jsonify(payload), 201)


@bp.route("/authorizations", methods=["GET"])
@token_required
def get_all(current_user):
    """Fetch all authorization relationships between Users and App_Groups from
    the Database.

    Returns
    -------
    response : <Response [200 OK]>
    {
        "authorizations": [
            {
                "created_by": created_by,
                "group_id": group_id,
                "id": id,
                "user_id": user_id
            }
        ],
        "current_user": current_user
    }
    """
    return make_response(
        jsonify(
            {
                "authorizations": authorization.get_all(),
                "current_user": current_user,
            }
        ),
        200,
    )
