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


# def get_one(user_id):
#     return (
#         get_db()
#         .execute(
#             """
#                 SELECT
#                     id,
#                     username,
#                     token
#                 FROM
#                     user
#                 WHERE
#                     id = ?
#             """,
#             (user_id),
#         )
#         .fetchone()
#     )

#     return cursor.lastrowid

# def update_token_by_id(id, token):
#     db_conn = get_db()
#     db_conn.execute(
#         """
#             UPDATE
#                 user
#             SET
#                 token = ?
#             WHERE
#                 id = ?
#         """,
#         (token, id),
#     )
#     db_conn.commit()

# def update_token_by_username(username, token):
#     db_conn = get_db()
#     db_conn.execute(
#         """
#             UPDATE
#                 user
#             SET
#                 token = ?
#             WHERE
#                 username = ?
#         """,
#         (token, username),
#     )
#     db_conn.commit()

# def delete_by_id(user_id):
#     db_conn = get_db()
#     db_conn.execute(
#         """
#             DELETE FROM
#                 user
#             WHERE id = ?
#         """,
#         (user_id,),
#     )
#     db_conn.commit()

# def delete_by_username(username):
#     db_conn = get_db()
#     db_conn.execute(
#         """
#             DELETE FROM
#                 user
#             WHERE username = ?
#         """,
#         (username),
#     )
#     db_conn.commit()
