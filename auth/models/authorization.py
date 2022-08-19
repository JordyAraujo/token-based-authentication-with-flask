from auth.db import get_db


def add(user_id, group_id, created_by):
    db_conn = get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        """
            INSERT INTO
                user_group_app (user_id, group_id, created_by)
            VALUES
                (?, ?, ?)
        """,
        (user_id, group_id, created_by),
    )
    db_conn.commit()
    pivot_id = cursor.lastrowid
    print(pivot_id)

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
