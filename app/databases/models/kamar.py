from app.databases.db_sql import db_sql


class KelasKamar(db_sql.Model):
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    kelas_kamar = db_sql.Column(db_sql.VARCHAR(32), nullable=False)
    nama_kelas = db_sql.Column(db_sql.VARCHAR(32), nullable=False)
    id_wisma = db_sql.Column(db_sql.Integer, nullable=False)


class Kamar(db_sql.Model):
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    nama_kamar = db_sql.Column(db_sql.VARCHAR(32), nullable=False)
    id_kelas_kamar = db_sql.Column(db_sql.Integer, nullable=False)
    kondisi = db_sql.Column(db_sql.VARCHAR(32), nullable=False)
    harga_kelas = db_sql.Column(db_sql.Integer, nullable=False)

    def insert(self, *args):
        