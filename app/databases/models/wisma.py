from app.databases.db_sql import db_sql


class Wisma(db_sql.Model):
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    nama_wisma = db_sql.Column(db_sql.VARCHAR(32))
    alamat_wisma = db_sql.Column(db_sql.VARCHAR(128))
