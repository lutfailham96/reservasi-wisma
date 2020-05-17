from app.databases.db_sql import db_sql
from app.utils.TimeUtils import datetime_jakarta


class Transaksi(db_sql.Model):
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    nama_konsumen = db_sql.Column(db_sql.VARCHAR(32))
    alamat_konsumen = db_sql.Column(db_sql.VARCHAR(128))
    kontak_konsumen = db_sql.Column(db_sql.VARCHAR(15))
    id_kamar = db_sql.Column(db_sql.INTEGER())
    id_kelas = db_sql.Column(db_sql.INTEGER())
    nominal = db_sql.Column(db_sql.INTEGER())
    tgl_booking = db_sql.Column(db_sql.DATETIME(), default=datetime_jakarta())
    tgl_awal = db_sql.Column(db_sql.DATETIME())
    tgl_akhir = db_sql.Column(db_sql.DATETIME())
    tgl_bayar = db_sql.Column(db_sql.DATETIME(), nullable=True)
    status_lunas = db_sql.Column(db_sql.INTEGER(), default=0)
    created = db_sql.Column(db_sql.DATETIME())
    updated = db_sql.Column(db_sql.DATETIME())

    def add_timestamp(self):
        self.created = datetime_jakarta()
        self.updated = self.created

    def update_timestamp(self):
        self.updated = datetime_jakarta()

    @staticmethod
    def del_transaksi(id_transaksi):
        data = Transaksi.query.get(id_transaksi)
        try:
            db_sql.session.delete(data)
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    def edit_transaksi(self):
        try:
            self.update_timestamp()
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    @staticmethod
    def add_transaksi(transaksi_data):
        try:
            transaksi_data.add_timestamp()
            db_sql.session.add(transaksi_data)
            db_sql.session.commit()
            return True
        except Exception:
            db_sql.session.rollback()
            db_sql.session.flush()
            return False
