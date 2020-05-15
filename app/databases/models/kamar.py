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
    def del_kelas_kamar(id_kelas_kamar):
        data = KelasKamar.query.get(id_kelas_kamar)
        try:
            db_sql.session.delete(data)
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    def edit_kelas_kamar(self):
        try:
            self.update_timestamp()
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    @staticmethod
    def add_kelas_kamar(kelas_kamar_data):
        try:
            kelas_kamar_data.add_timestamp()
            db_sql.session.add(kelas_kamar_data)
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
    def del_kamar(id_kamar):
        data = Kamar.query.get(id_kamar)
        try:
            db_sql.session.delete(data)
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    def edit_kamar(self):
        try:
            self.update_timestamp()
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    @staticmethod
    def add_kamar(kamar_data):
        try:
            kamar_data.add_timestamp()
            db_sql.session.add(kamar_data)
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False
