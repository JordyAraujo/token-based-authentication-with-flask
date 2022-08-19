from auth.db import get_db


def add(app_name, secret_key):
    db_conn = get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        """
            INSERT INTO
                secured_app (app_name, secret_key)
            VALUES
                (?, ?)
        """,
        (app_name, secret_key),
    )
    db_conn.commit()
    return cursor.lastrowid


def get_all():
    return (
        get_db()
        .execute(
            """
            SELECT
                id,
                app_name,
                secret_key
            FROM
                secured_app
        """
        )
        .fetchall()
    )


def by_name(app_name):
    return (
        get_db()
        .execute(
            """
                SELECT
                    id,
                    app_name,
                    secret_key
                FROM
                    secured_app
                WHERE
                    app_name = ?
            """,
            (app_name),
        )
        .fetchone()
    )
