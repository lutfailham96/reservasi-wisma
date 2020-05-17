from flask import Blueprint, redirect, url_for, render_template, request, flash, abort
from flask_login import current_user, login_user, login_required, logout_user
from app.admin.databases.models.kamar import Kamar, KelasKamar
from app.admin.databases.models.transaksi import Transaksi
from app.admin.databases.models.user import User
from app.admin.databases.models.wisma import Wisma
from app.admin.forms.kamar import KelasKamarForm, KamarForm
from app.admin.forms.login import LoginForm
from app.admin.forms.user import UserForm, UserProfileForm
from app.admin.forms.wisma import WismaForm
from app.databases import db_sql
from app.managers import csrf

bp_admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')


@bp_admin.route('/login', methods=['GET', 'POST'])
def login():
    # check user already login
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = LoginForm()
    # validate form on post
    if form.validate_on_submit():
        data = User.query.filter(User.username == form.username.data, User.password == form.password.data).first()
        if data is not None:
            # save user's session
            login_user(data)
            return redirect(url_for('admin.dashboard'))
        return render_template('login.html', form=form, invalid_credential=True)
    return render_template('login.html', form=form)


@bp_admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


@bp_admin.route('/home', methods=['GET'])
@login_required
def dashboard():
    dashboard_data = {
        'user': db_sql.session.query(User).count(),
        'kamar': db_sql.session.query(Kamar).count(),
        'wisma': db_sql.session.query(Wisma).count(),
        'transaksi': db_sql.session.query(Transaksi).count()
    }
    return render_template('dashboard.html', dashboard_sidebar='active', dashboard_data=dashboard_data)


@bp_admin.route('/home/user', methods=['GET', 'POST'])
@login_required
def user_data():
    users = User.query.all()
    return render_template('user_data.html', users=users, user_sidebar='active')


@bp_admin.route('/home/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
    form = UserForm()
    if form.validate_on_submit():
        data = User(
            username=form.username.data,
            password=form.password.data,
            nama=form.nama.data,
            jabatan=form.jabatan.data,
            status=form.status.data
        )
        # check username exists
        if User.check_username(form.username.data):
            return render_template('user_add.html', form=form, username_exist=True)
        # if add user success
        if User.add(data):
            flash('Data berhasil disimpan', 'success')
            return redirect(url_for('admin.user_data'))
        flash('Data gagal disimpan', 'error')
        return render_template('user_add.html', form=form)
    return render_template('user_add.html', form=form)


@bp_admin.route('/home/user/edit/<id_data>', methods=['GET', 'POST'])
@login_required
def user_update(id_data):
    data = User.query.get(id_data)
    # check user data is exist
    if data is None:
        return redirect(url_for('admin.user_data'))
    form = UserForm()
    # validate form post
    if form.validate_on_submit():
        data.nama = form.nama.data
        data.username = form.username.data
        data.jabatan = form.jabatan.data
        data.status = form.status.data
        # check if password changed
        if form.password.data.strip() != '':
            user_data.password = form.password.data
        # if edit data success
        if User.update(data):
            flash('Data berhasil diperbarui', 'success')
            return redirect(url_for('admin.user_data'))
        flash('Data gagal diperbarui', 'error')
        return render_template('user_update.html', data=data, form=form)
    return render_template('user_update.html', data=data, form=form)


@bp_admin.route('/home/wisma', methods=['GET', 'POST'])
@login_required
def wisma_data():
    wismas = Wisma.query.order_by(Wisma.nama_wisma).all()
    return render_template('wisma_data.html', wismas=wismas, wisma_sidebar='active')


@bp_admin.route('/home/wisma/edit/<id_data>', methods=['GET', 'POST'])
@login_required
def wisma_update(id_data):
    data = Wisma.query.get(id_data)
    # check wisma data is exist
    if data is None:
        return redirect(url_for('admin.wisma_data'))
    form = WismaForm()
    # validate form post
    if form.validate_on_submit():
        data.nama_wisma = form.nama_wisma.data
        data.alamat_wisma = form.alamat_wisma.data
        data.no_telp = form.no_telp.data
        # if edit data success
        if Wisma.update(data):
            flash('Data berhasil diperbarui', 'success')
            return redirect(url_for('admin.wisma_data'))
        return render_template('wisma_update.html', data=data, form=form)
    return render_template('wisma_update.html', data=data, form=form)


@bp_admin.route('/home/wisma/add', methods=['GET', 'POST'])
@login_required
def wisma_add():
    form = WismaForm()
    if form.validate_on_submit():
        data = Wisma(
            nama_wisma=form.nama_wisma.data,
            alamat_wisma=form.alamat_wisma.data,
            no_telp=form.no_telp.data
        )
        # if add wisma success
        if Wisma.add(data):
            flash('Data berhasil disimpan', 'success')
            return redirect(url_for('admin.wisma_data'))
        return render_template('wisma_add.html', form=form)
    return render_template('wisma_add.html', form=form)


@bp_admin.route('/home/transaksi', methods=['GET', 'POST'])
def transaksi():
    transaksis = db_sql.session.query(Transaksi, KelasKamar).join(KelasKamar, Transaksi.id_kelas == KelasKamar.id)
    return render_template('transaksi.html', transaksis=transaksis, transaksi_sidebar='active')


@bp_admin.route('/home/kelas_kamar')
def kelas_kamar_data():
    kelas_kamars = db_sql.session.query(KelasKamar, Wisma).join(Wisma, KelasKamar.id_wisma == Wisma.id)\
        .order_by(Wisma.nama_wisma, KelasKamar.nama_kelas)
    return render_template('kelas_kamar_data.html', kelas_kamars=kelas_kamars, kamar_sidebar='active',
                           kamar_kelas_kamar_menu='class=active')


@bp_admin.route('/home/kelas_kamar/edit/<id_data>', methods=['GET', 'POST'])
def kelas_kamar_update(id_data):
    data = KelasKamar.query.get(id_data)
    wismas = Wisma.query.all()
    # check kelas kamar data is exist
    if data is None:
        return redirect(url_for('admin.kelas_kamar_data'))
    form = KelasKamarForm()
    # validate form post
    if form.validate_on_submit():
        data.nama_kelas = form.nama_kelas.data
        data.id_wisma = form.id_wisma.data
        data.harga_kelas = form.harga_kelas.data
        # if edit data success
        if KelasKamar.update(data):
            flash('Data berhasil diperbarui', 'success')
            return redirect(url_for('admin.kelas_kamar_data'))
        return render_template('kelas_kamar_update.html', data=data, form=form)
    return render_template('kelas_kamar_update.html', data=data, wismas=wismas, form=form, kamar_sidebar='active',
                           kamar_kelas_kamar_menu='class=active')


@bp_admin.route('/home/kelas_kamar/add', methods=['GET', 'POST'])
@login_required
def kelas_kamar_add():
    form = KelasKamarForm()
    wismas = Wisma.query.all()
    if form.validate_on_submit():
        data = KelasKamar(
            nama_kelas=form.nama_kelas.data,
            id_wisma=form.id_wisma.data,
            harga_kelas=form.harga_kelas.data
        )
        # if add kelas kamar success
        if KelasKamar.add(data):
            flash('Data berhasil disimpan', 'success')
            return redirect(url_for('admin.kelas_kamar_data'))
        return render_template('kelas_kamar_add.html', wismas=wismas, form=form)
    return render_template('kelas_kamar_add.html', wismas=wismas, form=form, kamar_sidebar='active',
                           kamar_kelas_kamar_menu='class=active')


@bp_admin.route('/home/kamar', methods=['GET', 'POST'])
def kamar_data():
    kamars = db_sql.session.query(Kamar, KelasKamar).join(KelasKamar, Kamar.id_kelas_kamar == KelasKamar.id)
    return render_template('kamar_data.html', kamars=kamars, kamar_sidebar='active', kamar_kamar_menu='class=active')


@bp_admin.route('/home/kamar/edit/<id_data>', methods=['GET', 'POST'])
@login_required
def kamar_update(id_data):
    data = Kamar.query.get(id_data)
    kelas_kamars = KelasKamar.query.all()
    # check kelas kamar data is exist
    if data is None:
        return redirect(url_for('admin.kamar_data'))
    form = KamarForm()
    # validate form post
    if form.validate_on_submit():
        data.nama_kamar = form.nama_kamar.data
        data.id_kelas_kamar = form.id_kelas_kamar.data
        data.kondisi = form.kondisi.data
        # if edit data success
        if Kamar.update(data):
            flash('Data berhasil diperbarui', 'success')
            return redirect(url_for('admin.kamar_data'))
        return render_template('kamar_update.html', data=data, form=form)
    return render_template('kamar_update.html', data=data, kelas_kamars=kelas_kamars, form=form,
                           kamar_sidebar='active', kamar_kamar_menu='class=active')


@bp_admin.route('/home/kamar/add', methods=['GET', 'POST'])
@login_required
def kamar_add():
    form = KamarForm()
    kelas_kamars = KelasKamar.query.all()
    if form.validate_on_submit():
        data = Kamar(
            nama_kamar=form.nama_kamar.data,
            id_kelas_kamar=form.id_kelas_kamar.data,
            kondisi=form.kondisi.data
        )
        # if add wisma success
        if Kamar.add(data):
            flash('Data berhasil disimpan', 'success')
            return redirect(url_for('admin.kamar_data'))
        return render_template('kamar_add.html', kelas_kamars=kelas_kamars, form=form)
    return render_template('kamar_add.html', kelas_kamars=kelas_kamars, form=form, kamar_sidebar='active',
                           kamar_kamar_menu='class=active')


@bp_admin.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UserProfileForm()
    if request.method == 'POST':
        # user_data = User.query.get(int(current_user.id))
        # if len(str(form.password.data).strip()) > 0:
        #     user_data.password = form.password.data
        # user_data.nama = form.nama.data
        # if user_data.edit_user():
        #     return redirect(url_for('admin.profile'))
        flash('Update profile berhasil!', 'success')
        return redirect(url_for('admin.profile'))
    return render_template('profile.html', form=form)


@bp_admin.route('/ajax/kelas_kamar', methods=['GET', 'DELETE'])
@csrf.exempt
def ajax_kelas_kamar():
    if request.method == 'DELETE':
        id_data = request.get_json()['id']
        if KelasKamar.delete(id_data):
            return {
                       'success': True
                   }, 204
        abort(500)
    abort(500)


@bp_admin.route('/ajax/kamar', methods=['GET', 'DELETE'])
@csrf.exempt
def ajax_kamar():
    if request.method == 'DELETE':
        id_data = request.get_json()['id']
        if Kamar.delete(id_data):
            return {
                       'success': True
                   }, 204
        abort(500)
    abort(500)


@bp_admin.route('/ajax/user', methods=['GET', 'DELETE'])
@csrf.exempt
def ajax_user():
    if request.method == 'DELETE':
        id_data = request.get_json()['id']
        if User.delete(id_data):
            return {
                       'success': True
                   }, 204
        abort(500)
    abort(500)


@bp_admin.route('/ajax/wisma', methods=['GET', 'DELETE'])
@csrf.exempt
def ajax_wisma():
    if request.method == 'DELETE':
        id_data = request.get_json()['id']
        if Wisma.delete(id_data):
            return {
                       'success': True
                   }, 204
        abort(500)
    abort(500)
