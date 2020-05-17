from app.databases.db_sql import db_sql
from app.utils.TimeUtils import datetime_jakarta


class Wisma(db_sql.Model):
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    nama_wisma = db_sql.Column(db_sql.VARCHAR(32))
    alamat_wisma = db_sql.Column(db_sql.VARCHAR(128))
    no_telp = db_sql.Column(db_sql.VARCHAR(15))
    created = db_sql.Column(db_sql.DATETIME)
    updated = db_sql.Column(db_sql.DATETIME)

    def add_timestamp(self):
        self.created = datetime_jakarta()
        self.updated = self.created

    def update_timestamp(self):
        self.updated = datetime_jakarta()

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
            data = Wisma.query.get(id_data)
            db_sql.session.delete(data)
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

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
