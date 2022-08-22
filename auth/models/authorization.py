from auth.db import get_db


def add(user_id, group_id, created_by):
    """Create and Insert a new Secured App into the Database.

    Parameters
    ----------
    user_id : `int`
        ID of the User to be added to the Group.
    group_id : `int`
        ID of the Group to be added to the User.
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
                user_group_app (user_id, group_id, created_by)
            VALUES
                (?, ?, ?)
        """,
        (str(user_id), str(group_id), created_by),
    )
    db_conn.commit()
    pivot_id = cursor.lastrowid
    return cursor.execute(
        """
            SELECT
                user.username as username,
                app_group.group_name as app_group,
                secured_app.app_name as app_name
            FROM
                user_group_app
            INNER JOIN
                user
            ON
                user_group_app.user_id = user.id
            INNER JOIN
                app_group
            ON
                user_group_app.group_id = app_group.id
            INNER JOIN
                secured_app
            ON
                app_group.secured_app_id = secured_app.id
            WHERE
                user_group_app.id = ?
        """,
        [pivot_id],
    ).fetchone()


def get_all():
    """Get all Authorization Relationships from the Database.

    Returns
    -------
    [
        {
            "id": id,
            "user_id": user_id,
            "group_id": group_id,
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
                user_group_app
        """
        )
        .fetchall()
    )
