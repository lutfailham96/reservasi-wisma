from flask import flash
from flask_login import UserMixin, logout_user
from app.databases.db_sql import db_sql
from app.managers import login_manager
from app.utils.TimeUtils import datetime_jakarta
from werkzeug.security import generate_password_hash, check_password_hash


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
    def add(data):
        try:
            data.password = User.hash_password(data.password)
            data.add_timestamp()
            db_sql.session.add(data)
            db_sql.session.commit()
            return True
        except Exception as e:
            db_sql.session.rollback()
            db_sql.session.flush()
            print(e)
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
            data = User.query.get(id_data)
            db_sql.session.delete(data)
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

    @staticmethod
    def hash_password(password):
        hash_password = generate_password_hash(password)
        return hash_password

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def is_admin(id_data):
        if id_data == 0:
            return True
        return False

    @staticmethod
    def is_disabled(data):
        if data.status == 0:
            flash('User nonaktif')
            logout_user()
            return True
        return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
