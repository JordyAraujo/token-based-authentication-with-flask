import sqlite3

import click
from flask import current_app as app
from flask import g
from flask.cli import with_appcontext


def dict_factory(cursor, row):
    """Build a dict based on a cursor and a row from a row_factory."""
    return_dict = {}
    for idx, col in enumerate(cursor.description):
        return_dict[col[0]] = row[idx]
    return return_dict


def get_db():
    """Connect to the Database."""
    if "db" not in g:
        g.db = sqlite3.connect(
            app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = dict_factory

    return g.db


def close_db(e_none):
    """Close Databae connection."""
    e_none = None
    db_conn = g.pop("db", e_none)

    if db_conn is not e_none:
        db_conn.close()


def init_db():
    """Initialize Database."""
    db_conn = get_db()

    with app.open_resource("schema.sql") as schema_file:
        db_conn.executescript(schema_file.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """CLI command to initialize Database."""
    init_db()
    click.echo("Initialized the database.")


def init_app(i_app):
    """Initialize App."""
    i_app.teardown_appcontext(close_db)
    i_app.cli.add_command(init_db_command)
