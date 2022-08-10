import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def dict_factory(cursor, row):
    return_dict = {}
    for idx, col in enumerate(cursor.description):
        return_dict[col[0]] = row[idx]
    return return_dict


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = dict_factory

    return g.db


def close_db(e_none):
    e_none = None
    db_conn = g.pop("db", e_none)

    if db_conn is not e_none:
        db_conn.close()


def init_db():
    db_conn = get_db()

    with current_app.open_resource("schema.sql") as schema_file:
        db_conn.executescript(schema_file.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
