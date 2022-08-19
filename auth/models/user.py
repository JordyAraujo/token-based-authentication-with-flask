from auth.db import get_db


def add(username, token):
    db_conn = get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        """
            INSERT INTO
                user (username, token)
            VALUES
                (?, ?)
        """,
        (username, token),
    )
    db_conn.commit()


def get_token(username):
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
    db_conn = get_db()
    cursor = db_conn.cursor()
    return bool(
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


def get_all():
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
