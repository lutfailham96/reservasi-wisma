from flask import Flask, render_template

from app.databases.models.kamar import Kamar
from app.databases.models.wisma import Wisma
from config import Config
from app.databases import db_sql, init_database
from app.databases.models.user import User

app = Flask(__name__)
app.config.from_object(Config)


init_database(app)


@app.route('/')
def index():
    # data = User(
    #     username='test_username',
    #     password='test_password',
    #     jabatan='test_jabatan',
    #     status='test_status'
    # )
    # db_sql.session.add(data)
    # db_sql.session.commit()
    return 'Null'


@app.route('/admin/home', methods=['GET'])
def admin_dashboard():
    return render_template('admin/dashboard.html', dashboard_sidebar='active')


@app.route('/admin/home/user', methods=['GET', 'POST'])
def admin_user():
    users = User.query.all()
    app.logger.info(users)
    return render_template('admin/user.html', users=users, user_sidebar='active')


@app.route('/admin/home/transaksi', methods=['GET', 'POST'])
def admin_transaksi():
    pass


@app.route('/admin/home/kelas_kamar', methods=['GET', 'POST'])
def admin_kelas_kamar():
    pass


@app.route('/admin/home/kamar', methods=['GET', 'POST'])
def admin_kamar():
    kamars = Kamar.query.all()
    return render_template('admin/kamar.html', kamars=kamars, kamar_sidebar='active')


@app.route('/admin/home/wisma', methods=['GET', 'POST'])
def admin_wisma():
    wismas = Wisma.query.all()
    return render_template('admin/wisma.html', wismas=wismas, wisma_sidebar='active')
