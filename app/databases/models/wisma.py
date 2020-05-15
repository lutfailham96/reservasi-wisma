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
    def del_wisma(id_wisma):
        data = Wisma.query.get(id_wisma)
        try:
            db_sql.session.delete(data)
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    def edit_wisma(self):
        try:
            self.update_timestamp()
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    @staticmethod
    def add_wisma(wisma_data):
        try:
            wisma_data.add_timestamp()
            db_sql.session.add(wisma_data)
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False
