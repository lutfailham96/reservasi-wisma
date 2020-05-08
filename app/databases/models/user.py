from app.databases.db_sql import db_sql


class User(db_sql.Model):
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    username = db_sql.Column(db_sql.VARCHAR(32))
    password = db_sql.Column(db_sql.VARCHAR(32))
    jabatan = db_sql.Column(db_sql.VARCHAR(32))
    status = db_sql.Column(db_sql.VARCHAR(32))
