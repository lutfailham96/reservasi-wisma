from .db_sql import db_sql, db_migrate


def init_database(app):
    db_sql.init_app(app)
    db_migrate.init_app(app)
