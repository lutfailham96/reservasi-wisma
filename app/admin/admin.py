import os
from PIL import Image
from flask import Blueprint, redirect, url_for, render_template, request, flash, abort
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import text
from werkzeug.utils import secure_filename
from app.admin.databases.models.kamar import Kamar, KelasKamar
from app.admin.databases.models.transaksi import Transaksi
from app.admin.databases.models.user import User
from app.admin.databases.models.wisma import Wisma
from app.admin.forms.kamar import KelasKamarForm, KamarForm
from app.admin.forms.login import LoginForm
from app.admin.forms.user import UserForm, UserProfileForm
from app.admin.forms.wisma import WismaForm
from app.databases import db_sql
from app.managers.csrf import csrf

bp_admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')


# @bp_admin.after_request
# def add_header(r):
#     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r


@bp_admin.before_request
def check_disabled():
    if hasattr(current_user, 'id'):
        User.is_disabled(current_user)


@bp_admin.route('/login', methods=['GET', 'POST'])
def login():
    # check user already login
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = LoginForm()
    # post login form
    if form.validate_on_submit():
        data = User.query.filter_by(username=form.username.data).first()
        if data is not None and data.check_password(form.password.data):
            if User.is_disabled(data):
                return redirect(url_for('admin.login'))
            # save user's session
            login_user(data)
            return redirect(url_for('admin.dashboard'))
        # return render_template('login.html', form=form)
        flash('Kombinasi username dan password salah!', 'error')
        return redirect(url_for('admin.login'))
    return render_template('login.html', form=form)


@bp_admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


@bp_admin.route('/home')
@login_required
def dashboard():
    data = {
        'user': db_sql.session.query(User).count(),
        'kamar': db_sql.session.query(Kamar).count(),
        'wisma': db_sql.session.query(Wisma).count(),
        'transaksi': db_sql.session.query(Transaksi).count(),
        'kelas_kamar': db_sql.session.query(KelasKamar).count()
    }
    return render_template('dashboard.html', data=data, dashboard_sidebar='active')


@bp_admin.route('/home/user')
@login_required
def user_data():
    if not User.is_admin(current_user.jabatan):
        return redirect(url_for('admin.dashboard'))
    users = User.query.all()
    return render_template('user_data.html', users=users, user_sidebar='active')


@bp_admin.route('/home/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
    if not User.is_admin(current_user.jabatan):
        return redirect(url_for('admin.dashboard'))
    form = UserForm()
    # post user form
    if form.validate_on_submit():
        data = User(
            username=form.username.data,
            password=form.password.data,
            nama=form.nama.data,
            jabatan=form.jabatan.data,
            status=form.status.data
        )
        # check if username exists
        if User.check_username(form.username.data):
            return render_template('user_add.html', form=form, username_exist=True)
        # if add user success
        if User.add(data):
            flash('Data berhasil disimpan', 'success')
            return redirect(url_for('admin.user_data'))
        flash('Data gagal disimpan', 'error')
        # return render_template('user_add.html', form=form)
        return redirect(url_for('admin.user_add'))
    return render_template('user_add.html', form=form, user_sidebar='active')


@bp_admin.route('/home/user/edit/<id_data>', methods=['GET', 'POST'])
@login_required
def user_update(id_data):
    if not User.is_admin(current_user.jabatan):
        return redirect(url_for('admin.dashboard'))
    form = UserForm()
    data = User.query.get(id_data)
    # check if data exist
    if data is None:
        return redirect(url_for('admin.user_data'))
    # post user form
    if form.validate_on_submit():
        data.nama = form.nama.data
        data.username = form.username.data
        data.jabatan = form.jabatan.data
        data.status = form.status.data
        # check if password changed
        if len(form.password.data.strip()) > 0:
            data.password = User.hash_password(form.password.data)
        # if update data success
        if User.update(data):
            flash('Data berhasil diperbarui', 'success')
            return redirect(url_for('admin.user_data'))
        flash('Data gagal diperbarui', 'error')
        # return render_template('user_update.html', form=form, data=data)
        return redirect(url_for('admin.user_update'))
    return render_template('user_update.html', form=form, data=data, user_sidebar='active')


@bp_admin.route('/home/wisma')
@login_required
def wisma_data():
    wismas = Wisma.query.order_by(Wisma.nama_wisma).all()
    return render_template('wisma_data.html', wismas=wismas, wisma_sidebar='active')


@bp_admin.route('/home/wisma/edit/<id_data>', methods=['GET', 'POST'])
@login_required
def wisma_update(id_data):
    form = WismaForm()
    data = Wisma.query.get(id_data)
    # check if data is exist
    if data is None:
        return redirect(url_for('admin.wisma_data'))
    # post wisma form
    if form.validate_on_submit():
        data.nama_wisma = form.nama_wisma.data
        data.alamat_wisma = form.alamat_wisma.data
        data.no_telp = form.no_telp.data
        # if update data success
        if Wisma.update(data):
            flash('Data berhasil diperbarui', 'success')
            return redirect(url_for('admin.wisma_data'))
        # return render_template('wisma_update.html', form=form, data=data)
        redirect(url_for('admin.wisma_update'))
    return render_template('wisma_update.html', form=form, data=data, wisma_sidebar='active')


@bp_admin.route('/home/wisma/add', methods=['GET', 'POST'])
@login_required
def wisma_add():
    form = WismaForm()
    # post wisma form
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
        # return render_template('wisma_add.html', form=form)
        redirect(url_for('admin.wisma_add'))
    return render_template('wisma_add.html', form=form, wisma_sidebar='active')


@bp_admin.route('/home/transaksi')
@login_required
def transaksi():
    transaksis = db_sql.session.query(Transaksi, KelasKamar).join(KelasKamar, Transaksi.id_kelas == KelasKamar.id)
    return render_template('transaksi.html', transaksis=transaksis, transaksi_sidebar='active')


@bp_admin.route('/home/kelas_kamar')
@login_required
def kelas_kamar_data():
    kelas_kamars = db_sql.session.query(KelasKamar, Wisma).join(Wisma, KelasKamar.id_wisma == Wisma.id)\
        .order_by(Wisma.nama_wisma, KelasKamar.nama_kelas)
    return render_template('kelas_kamar_data.html', kelas_kamars=kelas_kamars, kamar_sidebar='active',
                           kelas_kamar_menu='active')


@bp_admin.route('/home/kelas_kamar/edit/<id_data>', methods=['GET', 'POST'])
@login_required
def kelas_kamar_update(id_data):
    form = KelasKamarForm()
    data = KelasKamar.query.get(id_data)
    wismas = Wisma.query.all()
    # check data is exist
    if data is None:
        return redirect(url_for('admin.kelas_kamar_data'))
    # post kelas kamar form
    if form.validate_on_submit():
        data.nama_kelas = form.nama_kelas.data
        data.id_wisma = form.id_wisma.data
        data.harga_kelas = form.harga_kelas.data.replace('.', '')
        # if update data success
        if KelasKamar.update(data):
            flash('Data berhasil diperbarui', 'success')
            return redirect(url_for('admin.kelas_kamar_data'))
        # return render_template('kelas_kamar_update.html', data=data, form=form)
        return redirect(url_for('admin.kelas_kamar_update'))
    return render_template('kelas_kamar_update.html', form=form, data=data, wismas=wismas, kamar_sidebar='active')


@bp_admin.route('/home/kelas_kamar/add', methods=['GET', 'POST'])
@login_required
def kelas_kamar_add():
    form = KelasKamarForm()
    wismas = Wisma.query.all()
    # post kelas kamar form
    if form.validate_on_submit():
        data = KelasKamar(
            nama_kelas=form.nama_kelas.data,
            id_wisma=form.id_wisma.data,
            harga_kelas=form.harga_kelas.data.replace('.', '')
        )
        # if add data success
        if KelasKamar.add(data):
            flash('Data berhasil disimpan', 'success')
            return redirect(url_for('admin.kelas_kamar_data'))
        # return render_template('kelas_kamar_add.html', form=form, wismas=wismas)
        return redirect(url_for('admin.kelas_kamar_add'))
    return render_template('kelas_kamar_add.html', form=form, wismas=wismas, kamar_sidebar='active')


@bp_admin.route('/home/kamar')
@login_required
def kamar_data():
    kamars = db_sql.session.query(Kamar, KelasKamar).join(KelasKamar, Kamar.id_kelas_kamar == KelasKamar.id)
    return render_template('kamar_data.html', kamars=kamars, kamar_sidebar='active', kamar_menu='active')


@bp_admin.route('/home/kamar/edit/<id_data>', methods=['GET', 'POST'])
@login_required
def kamar_update(id_data):
    form = KamarForm()
    data = Kamar.query.get(id_data)
    kelas_kamars = KelasKamar.query.all()
    # check data is exist
    if data is None:
        return redirect(url_for('admin.kamar_data'))
    # post kamar form
    if form.validate_on_submit():
        data.nama_kamar = form.nama_kamar.data
        data.id_kelas_kamar = form.id_kelas_kamar.data
        data.kondisi = form.kondisi.data
        # if update data success
        if Kamar.update(data):
            flash('Data berhasil diperbarui', 'success')
            return redirect(url_for('admin.kamar_data'))
        # return render_template('kamar_update.html', form=form, data=data)
        return redirect(url_for('admin.kamar_update'))
    return render_template('kamar_update.html', form=form, data=data, kelas_kamars=kelas_kamars, kamar_sidebar='active')


@bp_admin.route('/home/kamar/add', methods=['GET', 'POST'])
@login_required
def kamar_add():
    form = KamarForm()
    kelas_kamars = KelasKamar.query.all()
    # post kamar form
    if form.validate_on_submit():
        data = Kamar(
            nama_kamar=form.nama_kamar.data,
            id_kelas_kamar=form.id_kelas_kamar.data,
            kondisi=form.kondisi.data
        )
        # if add data success
        if Kamar.add(data):
            flash('Data berhasil disimpan', 'success')
            return redirect(url_for('admin.kamar_data'))
        # return render_template('kamar_add.html', form=form, kelas_kamars=kelas_kamars)
        return redirect(url_for('admin.kamar_add'))
    return render_template('kamar_add.html', form=form, kelas_kamars=kelas_kamars, kamar_sidebar='active')


@bp_admin.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UserProfileForm()
    if form.validate_on_submit():
        data = User.query.get(int(current_user.id))
        if len(str(form.password.data).strip()) > 0:
            data.password = User.hash_password(form.password.data)
        if len(str(form.nama.data).strip()) > 0:
            data.nama = form.nama.data
        if User.update(data):
            flash('Update profile berhasil!', 'success')
            return redirect(url_for('admin.profile'))
        return redirect(url_for('admin.profile'))
    return render_template('profile.html', form=form)


def allowed_file(filename):
    allowed = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


@bp_admin.route('/profile/photo', methods=['POST'])
@login_required
def profile_photo():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            upload_dir = '/app/admin/static/uploads/img'
            filename = secure_filename(str(current_user.id))
            file.save(os.path.join(os.getcwd() + upload_dir, filename + '_f.jpg'))
            # Compress image
            original_file = Image.open(os.path.join(os.getcwd() + upload_dir, filename + '_f.jpg'))
            original_file = original_file.convert('RGB')
            # medium size
            m_size = 160
            wpercent = (m_size / float(original_file.size[1]))
            hsize = int((float(original_file.size[0]) * float(wpercent)))
            med_file = original_file.resize((hsize, m_size), Image.ANTIALIAS)
            # med_file = original_file.resize((160, 160), Image.ANTIALIAS)
            med_file.save(os.path.join(os.getcwd() + upload_dir, filename + '_m.jpg'), optimze=True, quality=95)
            flash('Foto profile berhasil diubah', 'success')
            return redirect(url_for('admin.profile'))
        abort(403)


@bp_admin.route('/ajax/data/kelas_kamar', methods=['GET', 'DELETE'])
@login_required
@csrf.exempt
def ajax_data_kelas_kamar():
    if request.method == 'DELETE':
        id_data = request.get_json()['id']
        if KelasKamar.delete(id_data):
            return {
                       'success': True
                   }, 204
        abort(500)
    # get ajax request variable
    draw = int(request.args.get('draw'))
    per_page = int(request.args.get('length'))
    page = round((int(request.args.get('start')) / per_page) + 1)
    search_arg = request.args.get('search[value]')
    search = "%{}%".format(search_arg)
    items = ['kelas_kamar.id', 'kelas_kamar.nama_kelas', 'wisma.nama_wisma', 'kelas_kamar.harga_kelas']
    if int(request.args.get('order[0][column]')) >= len(items):
        order_by = items[0]
    else:
        order_by = items[int(request.args.get('order[0][column]'))]
    order_type = request.args.get('order[0][dir]')
    # paginate data
    list_data = db_sql.session.query(KelasKamar, Wisma).join(Wisma, KelasKamar.id_wisma == Wisma.id) \
        .order_by(text('{} {}'.format(order_by, order_type))).paginate(page, per_page, False)
    # if contains search keywords
    if len(str(search_arg).strip()) > 0:
        list_data = db_sql.session.query(KelasKamar, Wisma).join(Wisma, KelasKamar.id_wisma == Wisma.id) \
            .filter(KelasKamar.nama_kelas.like(search)).order_by(text('{} {}'.format(order_by, order_type)))\
            .paginate(page, per_page, False)
    total_count = db_sql.session.query(KelasKamar).count()
    filter_count = list_data.total
    data = []
    for index, item in enumerate(list_data.items):
        row = {
            'DT_RowId': item[0].id,
            'index': index + 1,
            'id': item[0].id,
            'nama_kelas': item[0].nama_kelas,
            'nama_wisma': item[1].nama_wisma,
            'id_wisma': item[0].id_wisma,
            'harga_kelas': item[0].harga_kelas
        }
        data.append(row)
    response = {
        "draw": draw,
        "recordsTotal": total_count,
        "recordsFiltered": filter_count,
        "data": data
    }
    return response


@bp_admin.route('/ajax/data/kamar', methods=['GET', 'DELETE'])
@login_required
@csrf.exempt
def ajax_data_kamar():
    if request.method == 'DELETE':
        id_data = request.get_json()['id']
        if Kamar.delete(id_data):
            return {
                       'success': True
                   }, 204
        abort(500)
    # get ajax request variable
    draw = int(request.args.get('draw'))
    per_page = int(request.args.get('length'))
    page = round((int(request.args.get('start')) / per_page) + 1)
    search_arg = request.args.get('search[value]')
    search = "%{}%".format(search_arg)
    items = ['kamar.id', 'kamar.nama_kamar', 'kelas_kamar.nama_kelas', 'kamar.kondisi', 'kelas_kamar.harga_kelas']
    if int(request.args.get('order[0][column]')) >= len(items):
        order_by = items[0]
    else:
        order_by = items[int(request.args.get('order[0][column]'))]
    order_type = request.args.get('order[0][dir]')
    # paginate data
    list_data = db_sql.session.query(Kamar, KelasKamar).join(KelasKamar, Kamar.id_kelas_kamar == KelasKamar.id) \
        .order_by(text('{} {}'.format(order_by, order_type))).paginate(page, per_page, False)
    # if contains search keywords
    if len(str(search_arg).strip()) > 0:
        list_data = db_sql.session.query(Kamar, KelasKamar).join(KelasKamar, Kamar.id_kelas_kamar == KelasKamar.id) \
            .filter(Kamar.nama_kamar.like(search)).order_by(text('{} {}'.format(order_by, order_type))) \
            .paginate(page, per_page, False)
    total_count = db_sql.session.query(Kamar).count()
    filter_count = list_data.total
    data = []
    for index, item in enumerate(list_data.items):
        row = {
            'DT_RowId': item[0].id,
            'index': index + 1,
            'id': item[0].id,
            'nama_kamar': item[0].nama_kamar,
            'nama_kelas': item[1].nama_kelas,
            'kondisi': item[0].kondisi,
            'harga_kelas': item[1].harga_kelas
        }
        data.append(row)
    response = {
        "draw": draw,
        "recordsTotal": total_count,
        "recordsFiltered": filter_count,
        "data": data
    }
    return response


@bp_admin.route('/ajax/data/user', methods=['GET', 'DELETE'])
@login_required
@csrf.exempt
def ajax_data_user():
    if not User.is_admin(current_user.jabatan):
        abort(403)
    if request.method == 'DELETE':
        id_data = request.get_json()['id']
        if User.delete(id_data):
            return {
                       'success': True
                   }, 204
        abort(500)
        # get ajax request variable
    draw = int(request.args.get('draw'))
    per_page = int(request.args.get('length'))
    page = round((int(request.args.get('start')) / per_page) + 1)
    search_arg = request.args.get('search[value]')
    search = "%{}%".format(search_arg)
    items = ['user.id', 'user.nama', 'user.username', 'user.jabatan', 'user.status']
    if int(request.args.get('order[0][column]')) >= len(items):
        order_by = items[0]
    else:
        order_by = items[int(request.args.get('order[0][column]'))]
    order_type = request.args.get('order[0][dir]')
    # paginate data
    list_data = User.query.order_by(text('{} {}'.format(order_by, order_type))).paginate(page, per_page, False)
    # if contains search keywords
    if len(str(search_arg).strip()) > 0:
        list_data = User.query.filter(User.nama.like(search)) \
            .order_by(text('{} {}'.format(order_by, order_type))).paginate(page, per_page, False)
    total_count = db_sql.session.query(User).count()
    filter_count = list_data.total
    data = []
    for index, item in enumerate(list_data.items):
        row = {
            'DT_RowId': item.id,
            'index': index + 1,
            'id': item.id,
            'nama': item.nama,
            'username': item.username,
            'jabatan': item.jabatan,
            'status': item.status
        }
        data.append(row)
    response = {
        "draw": draw,
        "recordsTotal": total_count,
        "recordsFiltered": filter_count,
        "data": data
    }
    return response


@bp_admin.route('/ajax/data/wisma', methods=['GET', 'DELETE'])
@login_required
@csrf.exempt
def ajax_data_wisma():
    if request.method == 'DELETE':
        id_data = request.get_json()['id']
        if Wisma.delete(id_data):
            return {
                       'success': True
                   }, 204
        abort(500)
    # get ajax request variable
    draw = int(request.args.get('draw'))
    per_page = int(request.args.get('length'))
    page = round((int(request.args.get('start')) / per_page) + 1)
    search_arg = request.args.get('search[value]')
    search = "%{}%".format(search_arg)
    items = ['wisma.id', 'wisma.nama_wisma', 'wisma.alamat_wisma', 'wisma.no_telp']
    if int(request.args.get('order[0][column]')) >= len(items):
        order_by = items[0]
    else:
        order_by = items[int(request.args.get('order[0][column]'))]
    order_type = request.args.get('order[0][dir]')
    # paginate data
    list_data = Wisma.query.order_by(text('{} {}'.format(order_by, order_type))).paginate(page, per_page, False)
    # if contains search keywords
    if len(str(search_arg).strip()) > 0:
        list_data = Wisma.query.filter(Wisma.nama_wisma.like(search))\
            .order_by(text('{} {}'.format(order_by, order_type))).paginate(page, per_page, False)
    total_count = db_sql.session.query(Wisma).count()
    filter_count = list_data.total
    data = []
    for index, item in enumerate(list_data.items):
        row = {
            'DT_RowId': item.id,
            'index': index + 1,
            'id': item.id,
            'nama_wisma': item.nama_wisma,
            'alamat_wisma': item.alamat_wisma,
            'no_telp': item.no_telp,
        }
        data.append(row)
    response = {
        "draw": draw,
        "recordsTotal": total_count,
        "recordsFiltered": filter_count,
        "data": data
    }
    return response
