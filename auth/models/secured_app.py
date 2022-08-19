from auth.db import get_db


def add(app_name, created_by):
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
    return cursor.lastrowid


def get_all():
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
            (app_id),
        )
        .fetchone()
    )


def by_name(app_name):
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
            (app_name),
        )
        .fetchone()
    )
