import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import CSRFProtect
from app.databases.models.kamar import Kamar, KelasKamar
from app.databases.models.transaksi import Transaksi
from app.databases.models.wisma import Wisma
from app.forms.kamar import KelasKamarDelForm, KelasKamarForm, KamarForm, KamarDelForm
from app.forms.login import LoginForm
from app.forms.transaksi import TransaksiForm
from app.forms.user import UserForm, UserDelForm, UserProfileForm
from app.databases import db_sql, init_database
from app.databases.models.user import User
from app.forms.wisma import WismaDelForm, WismaForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = "admin_login"
csrf = CSRFProtect(app)
init_database(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # check already login
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    form = LoginForm()
    # validate form on post
    if form.validate_on_submit():
        user_data = User.query.filter(User.username == form.username.data, User.password == form.password.data).first()
        if user_data is not None:
            # save user's session
            login_user(user_data)
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/login.html', form=form, invalid_credential=True)
    return render_template('admin/login.html', form=form)


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))


@app.route('/admin/home', methods=['GET'])
@login_required
def admin_dashboard():
    dashboard_data = {
        'user': db_sql.session.query(User).count(),
        'kamar': db_sql.session.query(Kamar).count(),
        'wisma': db_sql.session.query(Wisma).count(),
        'transaksi': db_sql.session.query(Transaksi).count()
    }
    return render_template('admin/dashboard.html', dashboard_sidebar='active', dashboard_data=dashboard_data)


@app.route('/admin/home/user', methods=['GET', 'POST'])
@login_required
def admin_user_data():
    users = User.query.all()
    form = UserDelForm()
    return render_template('admin/user_data.html', users=users, form=form, user_sidebar='active')


@app.route('/admin/home/user/del', methods=['POST'])
@login_required
def admin_user_del():
    id_user = request.form.get('id_user')
    if User.del_user(id_user):
        flash('Data berhasil dihapus', 'success')
        return redirect(url_for('admin_user_data'))
    flash('Data gagal dihapus', 'error')
    return redirect(url_for('admin_user_data'))


@app.route('/admin/home/user/add', methods=['GET', 'POST'])
@login_required
def admin_user_add():
    form = UserForm()
    if form.validate_on_submit():
        user_data = User(
            username=form.username.data,
            password=form.password.data,
            nama=form.nama.data,
            jabatan=form.jabatan.data,
            status=form.status.data
        )
        # check username exists
        if User.check_username(form.username.data):
            return render_template('admin/user_add.html', user_data=user_data, form=form, username_exist=True)
        # if add user success
        if User.add_user(user_data):
            flash('Data berhasil disimpan', 'success')
            return redirect(url_for('admin_user_data'))
        flash('Data gagal disimpan', 'error')
        return render_template('admin/user_add.html', user_data=user_data, form=form)
    return render_template('admin/user_add.html', user_data=None, form=form)


@app.route('/admin/home/user/edit/<id_user>', methods=['GET', 'POST'])
@login_required
def admin_user_edit(id_user):
    user_data = User.query.get(id_user)
    # check user data is exist
    if user_data is None:
        return redirect(url_for('admin_user_data'))
    form = UserForm()
    # validate form post
    if form.validate_on_submit():
        user_data.nama = form.nama.data
        user_data.username = form.username.data
        user_data.jabatan = form.jabatan.data
        user_data.status = form.status.data
        # check if password changed
        if form.password.data.strip() != '':
            user_data.password = form.password.data
        # if edit data success
        if user_data.edit_user():
            flash('Data berhasil diperbarui', 'success')
            return redirect(url_for('admin_user_data'))
        flash('Data gagal diperbarui', 'error')
        return render_template('admin/user_edit.html', user_data=user_data, form=form)
    return render_template('admin/user_edit.html', user_data=user_data, form=form)


@app.route('/admin/home/wisma', methods=['GET', 'POST'])
@login_required
def admin_wisma_data():
    wismas = Wisma.query.order_by(Wisma.nama_wisma).all()
    form = WismaDelForm()
    return render_template('admin/wisma_data.html', wismas=wismas, form=form, wisma_sidebar='active')


@app.route('/admin/home/wisma/del', methods=['POST'])
@login_required
def admin_wisma_del():
    form = WismaDelForm()
    if Wisma.del_wisma(form.id_wisma.data):
        flash('Data berhasil dihapus', 'success')
        return redirect(url_for('admin_wisma_data'))
    flash('Data gagal dihapus', 'error')
    return redirect(url_for('admin_wisma_data'))


@app.route('/admin/home/wisma/edit/<id_wisma>', methods=['GET', 'POST'])
@login_required
def admin_wisma_edit(id_wisma):
    wisma_data = Wisma.query.get(id_wisma)
    # check wisma data is exist
    if wisma_data is None:
        return redirect(url_for('admin_wisma_data'))
    form = WismaForm()
    # validate form post
    if form.validate_on_submit():
        wisma_data.nama_wisma = form.nama_wisma.data
        wisma_data.alamat_wisma = form.alamat_wisma.data
        wisma_data.no_telp = form.no_telp.data
        # if edit data success
        if wisma_data.edit_wisma():
            flash('Data berhasil diperbarui', 'success')
            return redirect(url_for('admin_wisma_data'))
        return render_template('admin/wisma_edit.html', wisma_data=wisma_data, form=form)
    return render_template('admin/wisma_edit.html', wisma_data=wisma_data, form=form)


@app.route('/admin/home/wisma/add', methods=['GET', 'POST'])
@login_required
def admin_wisma_add():
    form = WismaForm()
    if form.validate_on_submit():
        wisma_data = Wisma(
            nama_wisma=form.nama_wisma.data,
            alamat_wisma=form.alamat_wisma.data,
            no_telp=form.no_telp.data
        )
        # if add wisma success
        if Wisma.add_wisma(wisma_data):
            flash('Data berhasil disimpan', 'success')
            return redirect(url_for('admin_wisma_data'))
        return render_template('admin/wisma_add.html', wisma_data=wisma_data, form=form)
    return render_template('admin/wisma_add.html', wisma_data=None, form=form)


@app.route('/admin/home/transaksi', methods=['GET', 'POST'])
def admin_transaksi():
    transaksis = db_sql.session.query(Transaksi, KelasKamar).join(KelasKamar, Transaksi.id_kelas == KelasKamar.id)
    return render_template('admin/transaksi.html', transaksis=transaksis, transaksi_sidebar='active')


@app.route('/admin/home/kelas_kamar', methods=['GET', 'POST'])
@login_required
def admin_kelas_kamar_data():
    kelas_kamars = db_sql.session.query(KelasKamar, Wisma).join(Wisma, KelasKamar.id_wisma == Wisma.id).order_by(Wisma.nama_wisma)
    form = KelasKamarDelForm()
    return render_template('admin/kelas_kamar_data.html', kelas_kamars=kelas_kamars, form=form, kamar_sidebar='active', kamar_kelas_kamar_menu='class=active')


@app.route('/admin/home/kelas_kamar/del', methods=['POST'])
@login_required
def admin_kelas_kamar_del():
    form = KelasKamarDelForm()
    if KelasKamar.del_kelas_kamar(form.id_kelas_kamar.data):
        flash('Data berhasil dihapus', 'success')
        return redirect(url_for('admin_kelas_kamar_data'))
    flash('Data gagal dihapus', 'error')
    return redirect(url_for('admin_kelas_kamar_data'))


@app.route('/admin/home/kelas_kamar/edit/<id_kelas_kamar>', methods=['GET', 'POST'])
@login_required
def admin_kelas_kamar_edit(id_kelas_kamar):
    kelas_kamar_data = KelasKamar.query.get(id_kelas_kamar)
    wismas = Wisma.query.all()
    # check kelas kamar data is exist
    if kelas_kamar_data is None:
        return redirect(url_for('admin_kelas_kamar_data'))
    form = KelasKamarForm()
    # validate form post
    if form.validate_on_submit():
        kelas_kamar_data.nama_kelas = form.nama_kelas.data
        kelas_kamar_data.id_wisma = form.id_wisma.data
        kelas_kamar_data.harga_kelas = form.harga_kelas.data
        # if edit data success
        if kelas_kamar_data.edit_kelas_kamar():
            flash('Data berhasil diperbarui', 'success')
            return redirect(url_for('admin_kelas_kamar_data'))
        return render_template('admin/kelas_kamar_edit.html', kelas_kamar_data=kelas_kamar_data, form=form)
    return render_template('admin/kelas_kamar_edit.html', kelas_kamar_data=kelas_kamar_data, wismas=wismas, form=form, kamar_sidebar='active', kamar_kelas_kamar_menu='class=active')


@app.route('/admin/home/kelas_kamar/add', methods=['GET', 'POST'])
@login_required
def admin_kelas_kamar_add():
    form = KelasKamarForm()
    wismas = Wisma.query.all()
    if form.validate_on_submit():
        kelas_kamar_data = KelasKamar(
            nama_kelas=form.nama_kelas.data,
            id_wisma=form.id_wisma.data,
            harga_kelas=form.harga_kelas.data
        )
        # if add kelas kamar success
        if KelasKamar.add_kelas_kamar(kelas_kamar_data):
            flash('Data berhasil disimpan', 'success')
            return redirect(url_for('admin_kelas_kamar_data'))
        return render_template('admin/kelas_kamar_add.html', kelas_kamar_data=kelas_kamar_data, wismas=wismas, form=form)
    return render_template('admin/kelas_kamar_add.html', kelas_kamar_data=None, wismas=wismas, form=form, kamar_sidebar='active', kamar_kelas_kamar_menu='class=active')


@app.route('/admin/home/kamar', methods=['GET', 'POST'])
def admin_kamar_data():
    form = KamarDelForm()
    kamars = db_sql.session.query(Kamar, KelasKamar).join(KelasKamar, Kamar.id_kelas_kamar == KelasKamar.id)
    return render_template('admin/kamar_data.html', form=form, kamars=kamars, kamar_sidebar='active', kamar_kamar_menu='class=active')


@app.route('/admin/home/kamar/edit/<id_kamar>', methods=['GET', 'POST'])
@login_required
def admin_kamar_edit(id_kamar):
    kamar_data = Kamar.query.get(id_kamar)
    kelas_kamars = KelasKamar.query.all()
    # check kelas kamar data is exist
    if kamar_data is None:
        return redirect(url_for('admin_kamar_data'))
    form = KamarForm()
    # validate form post
    if form.validate_on_submit():
        kamar_data.nama_kamar = form.nama_kamar.data
        kamar_data.id_kelas_kamar = form.id_kelas_kamar.data
        kamar_data.kondisi = form.kondisi.data
        # if edit data success
        if kamar_data.edit_kamar():
            flash('Data berhasil diperbarui', 'success')
            return redirect(url_for('admin_kamar_data'))
        return render_template('admin/kamar_edit.html', kamar_data=kamar_data, form=form)
    return render_template('admin/kamar_edit.html', kamar_data=kamar_data, kelas_kamars=kelas_kamars, form=form, kamar_sidebar='active', kamar_kamar_menu='class=active')


@app.route('/admin/home/kamar/add', methods=['GET', 'POST'])
@login_required
def admin_kamar_add():
    form = KamarForm()
    kelas_kamars = KelasKamar.query.all()
    if form.validate_on_submit():
        kamar_data = Kamar(
            nama_kamar=form.nama_kamar.data,
            id_kelas_kamar=form.id_kelas_kamar.data,
            kondisi=form.kondisi.data
        )
        # if add wisma success
        if Kamar.add_kamar(kamar_data):
            flash('Data berhasil disimpan', 'success')
            return redirect(url_for('admin_kamar_data'))
        return render_template('admin/kamar_add.html', kamar_data=kamar_data, kelas_kamars=kelas_kamars, form=form)
    return render_template('admin/kamar_add.html', kamar_data=None, kelas_kamars=kelas_kamars, form=form, kamar_sidebar='active', kamar_kamar_menu='class=active')


@app.route('/admin/home/kamar/del', methods=['POST'])
@login_required
def admin_kamar_del():
    form = KamarDelForm()
    if Kamar.del_kamar(form.id_kamar.data):
        flash('Data berhasil dihapus', 'success')
        return redirect(url_for('admin_kamar_data'))
    flash('Data gagal dihapus', 'error')
    return redirect(url_for('admin_kamar_data'))


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


@app.route('/api/kelas', methods=['POST'])
@csrf.exempt
def api_kelas():
    id_wisma = request.form.get('id_wisma')
    kelas_kamars = KelasKamar.query.filter_by(id_wisma=id_wisma).order_by(KelasKamar.nama_kelas)
    if kelas_kamars is not None:
        data = [data.to_dict() for data in kelas_kamars]
        return jsonify(data)
    return 'None', 404


@app.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    form = UserProfileForm()
    if request.method == 'POST':
        # user_data = User.query.get(int(current_user.id))
        # if len(str(form.password.data).strip()) > 0:
        #     user_data.password = form.password.data
        # user_data.nama = form.nama.data
        # if user_data.edit_user():
        #     return redirect(url_for('admin_profile'))
        flash('Update profile berhasil!', 'success')
        return redirect(url_for('admin_profile'))
    return render_template('admin/profile.html', form=form)
