from flask_login import UserMixin
from app.databases.db_sql import db_sql
from app.utils.TimeUtils import datetime_jakarta


class User(db_sql.Model, UserMixin):
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    username = db_sql.Column(db_sql.VARCHAR(32), unique=True)
    password = db_sql.Column(db_sql.VARCHAR(32))
    nama = db_sql.Column(db_sql.VARCHAR(32))
    jabatan = db_sql.Column(db_sql.INTEGER())
    status = db_sql.Column(db_sql.INTEGER())
    created = db_sql.Column(db_sql.DATETIME())
    updated = db_sql.Column(db_sql.DATETIME())

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
            data = User.query.get(id_data)
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

    @staticmethod
    def check_username(username):
        data = User.query.filter_by(username=username).first()
        if data is not None:
            return True
        return False