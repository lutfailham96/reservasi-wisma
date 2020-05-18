import datetime
from app.admin.admin import bp_admin
from app.admin.forms.transaksi import TransaksiForm
from app.admin.databases.models.kamar import Kamar
from app.admin.databases.models.transaksi import Transaksi
from app.admin.databases.models.wisma import Wisma
from app.admin.forms.login import LoginForm
from app.databases import db_sql, init_database
from app.managers import init_manager
from app.api.api import bp_api
from config import Config
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(bp_admin, url_prefix='/admin')
app.register_blueprint(bp_api, url_prefix='/api')
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True
init_database(app)
init_manager(app)


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    form = TransaksiForm()
    if request.method == 'POST':
        nama = form.nama_konsumen.data
        alamat = form.alamat_konsumen.data
        kontak = form.kontak_konsumen.data
        # tanggal = form.tanggal.data.split(' - ')
        # a_tanggal = tanggal[0].split(' ')
        # e_tanggal = tanggal[1].split(' ')
        # a_M, a_D, a_Y = a_tanggal[0].split('/')
        # a_h, a_m = a_tanggal[1].split(':')
        # e_M, e_D, e_Y = e_tanggal[0].split('/')
        # e_h, e_m = e_tanggal[1].split(':')
        # awal = datetime.datetime(int(a_Y), int(a_M), int(a_D), int(a_h), int(a_m))
        # akhir = datetime.datetime(int(e_Y), int(e_M), int(e_D), int(e_h), int(e_m))
        tanggal = form.tanggal.data.split(' - ')
        a_tanggal = tanggal[0]
        e_tanggal = tanggal[1]
        a_M, a_D, a_Y = a_tanggal.split('/')
        e_M, e_D, e_Y = e_tanggal.split('/')
        awal = datetime.datetime(int(a_Y), int(a_M), int(a_D), int(14), int(00))
        akhir = datetime.datetime(int(e_Y), int(e_M), int(e_D), int(12), int(00))
        id_kelas = form.id_kelas.data
        transaksi_data = Transaksi(
            nama_konsumen=nama,
            alamat_konsumen=alamat,
            kontak_konsumen=kontak,
            id_kelas=id_kelas,
            tgl_awal=awal,
            tgl_akhir=akhir
        )
        # db_sql.session.add(transaksi_data)
        # db_sql.session.commit()
        if Transaksi.add_transaksi(transaksi_data):
            flash('Booking kamar sukes, silahkan menunggu pesan konfirmasi pembayaran')
            return redirect(url_for('booking'))
        return redirect(url_for('booking'))
    kamars = Kamar.query.filter_by(kondisi=0).order_by(Kamar.nama_kamar)
    wismas = Wisma.query.order_by(Wisma.nama_wisma).all()
    return render_template('form_booking.html', wismas=wismas, form=form)
