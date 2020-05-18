from app.databases.db_sql import db_sql
from app.utils.TimeUtils import datetime_jakarta


class KelasKamar(db_sql.Model):
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    nama_kelas = db_sql.Column(db_sql.VARCHAR(32))
    id_wisma = db_sql.Column(db_sql.INTEGER())
    harga_kelas = db_sql.Column(db_sql.INTEGER())
    created = db_sql.Column(db_sql.DATETIME())
    updated = db_sql.Column(db_sql.DATETIME())

    def add_timestamp(self):
        self.created = datetime_jakarta()
        self.updated = self.created

    def update_timestamp(self):
        self.updated = datetime_jakarta()

    @staticmethod
    def add(data):
        try:
            data.add_timestamp()
            db_sql.session.add(data)
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    @staticmethod
    def update(data):
        try:
            data.update_timestamp()
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    @staticmethod
    def delete(id_data):
        try:
            data = KelasKamar.query.get(id_data)
            db_sql.session.delete(data)
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    def to_dict(self):
        return {
            'id': self.id,
            'nama_kelas': self.nama_kelas,
            'harga_kelas': self.harga_kelas
        }


class Kamar(db_sql.Model):
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    nama_kamar = db_sql.Column(db_sql.VARCHAR(32))
    id_kelas_kamar = db_sql.Column(db_sql.INTEGER())
    kondisi = db_sql.Column(db_sql.INTEGER())
    created = db_sql.Column(db_sql.DATETIME())
    updated = db_sql.Column(db_sql.DATETIME())

    def add_timestamp(self):
        self.created = datetime_jakarta()
        self.updated = self.created

    def update_timestamp(self):
        self.updated = datetime_jakarta()

    @staticmethod
    def add(data):
        try:
            data.add_timestamp()
            db_sql.session.add(data)
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    @staticmethod
    def update(data):
        try:
            data.update_timestamp()
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    @staticmethod
    def delete(id_data):
        try:
            data = Kamar.query.get(id_data)
            db_sql.session.delete(data)
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False
