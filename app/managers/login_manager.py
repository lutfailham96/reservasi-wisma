from flask_login import LoginManager

login_manager = LoginManager()
login_manager.blueprint_login_views = {
    'admin': '/admin/login'
}
