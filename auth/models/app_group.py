from auth.db import get_db


def add(group_name, secured_app_id, created_by):
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
