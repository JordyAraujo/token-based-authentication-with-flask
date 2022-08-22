from auth.db import get_db


def add(group_name, secured_app_id, created_by):
    """Create and Insert a new Secured App into the Database.

    Parameters
    ----------
    group_name : `str`
        Name of the Group to be created.
    secured_app_id : `int`
        ID of the App to be Secured by the Group.
    created_by : `str`
        Username of the User creating the authorization relationship.

    Returns
    -------
    {
        "app_group": app_group,
        "app_name": app_name,
        "username": username
    }
    """
    db_conn = get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        """
            INSERT INTO
                app_group (group_name, secured_app_id, created_by)
            VALUES
                (?, ?, ?)
        """,
        (group_name, secured_app_id, created_by),
    )
    db_conn.commit()
    return cursor.lastrowid


def get_all():
    """Get all Authorization Groups from the Database.

    Returns
    -------
    [
        {
            "id": id,
            "app_name": app_name,
            "created_by": created_by
        }
    ]
    """
    return (
        get_db()
        .execute(
            """
            SELECT
                *
            FROM
                secured_app
        """
        )
        .fetchall()
    )
