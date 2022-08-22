import jwt
from flask import current_app as app

from auth.db import get_db


def add(username_and_password):
    """Create and Insert a new User into the Database.

    Parameters
    ----------
    username : `str`
        Username for the user to be created.
    token : `str`
        Password for the user to be created.

    Returns
    -------
    token : `str`
        Token for the created User
    """
    token = jwt.encode(username_and_password, app.config.SECRET_KEY, "HS256")
    db_conn = get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        """
            INSERT INTO
                user (username, token)
            VALUES
                (?, ?)
        """,
        (username_and_password["username"], token),
    )
    db_conn.commit()
    return token


def get_token(username):
    """Get user Token from the Database.

    Parameters
    ----------
    username : `str`
        Username for the user to be selected.

    Returns
    -------
    {
        "token": token
    }
    """
    db_conn = get_db()
    cursor = db_conn.cursor()
    return cursor.execute(
        """
            SELECT
                token
            FROM
                user
            WHERE
                username = ?
        """,
        [username],
    ).fetchone()


def token_exists(token):
    """Check on the Database if the User exists.

    Parameters
    ----------
    token : `str`
        Token for the user to be checked.

    Returns
    -------
    exists : `boolean`
        True if the User exists on the Database.
    """
    db_conn = get_db()
    cursor = db_conn.cursor()
    exists = bool(
        cursor.execute(
            """
            SELECT
                1
            FROM
                user
            WHERE
                token = ?
        """,
            [token],
        ).fetchone()
    )
    return exists


def get_all():
    """Get all Users from the Database.

    Returns
    -------
    [
        {
            "id": id,
            "username": username,
            "token": token
        }
    ]
    """
    return (
        get_db()
        .execute(
            """
                SELECT
                    id,
                    username,
                    token
                FROM
                    user
            """
        )
        .fetchall()
    )
