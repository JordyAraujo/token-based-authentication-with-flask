from auth.db import get_db


def add(app_name, created_by):
    """Create and Insert a new Secured App into the Database.

    Parameters
    ----------
    app_name : `str`
        Name for the App to be Secured.
    created_by : `str`
        User creating the App.

    Returns
    -------
    app_id : `int`
        ID for the Secured App
    """
    db_conn = get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        """
            INSERT INTO
                secured_app (app_name, created_by)
            VALUES
                (?, ?)
        """,
        (app_name, created_by),
    )
    db_conn.commit()
    app_id = cursor.lastrowid
    return app_id


def get_all():
    """Get all Secured Apps from the Database.

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


def by_id(app_id):
    """Get a Secured App from the Database.

    Parameters
    ----------
    app_id : `int`
        ID of the App to be selected.

    Returns
    -------
    {
        "id": id,
        "app_name": app_name,
        "created_by": created_by
    }
    """
    return (
        get_db()
        .execute(
            """
                SELECT
                    *
                FROM
                    secured_app
                WHERE
                    id = ?
            """,
            [str(app_id)],
        )
        .fetchone()
    )


def by_name(app_name):
    """Get a Secured App from the Database.

    Parameters
    ----------
    app_name : `str`
        Name of the App to be selected.

    Returns
    -------
    {
        "id": id,
        "app_name": app_name,
        "created_by": created_by
    }
    """
    return (
        get_db()
        .execute(
            """
                SELECT
                    *
                FROM
                    secured_app
                WHERE
                    app_name = ?
            """,
            [app_name],
        )
        .fetchone()
    )
