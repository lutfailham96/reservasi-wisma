from app.managers.csrf import csrf
from app.managers.login_manager import login_manager


def init_manager(app):
    login_manager.init_app(app)
    csrf.init_app(app)
