from flask_login import LoginManager
from flask_wtf import CSRFProtect
from app.admin.databases.models.user import User

login_manager = LoginManager()
login_manager.blueprint_login_views = {
    'admin': '/admin/login'
}
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def init_manager(app):
    login_manager.init_app(app)
    csrf.init_app(app)
