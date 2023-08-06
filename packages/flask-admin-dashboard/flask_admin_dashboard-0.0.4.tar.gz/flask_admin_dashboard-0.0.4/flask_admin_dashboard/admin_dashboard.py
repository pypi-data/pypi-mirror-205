import os, shutil
from flask_admin import Admin
from flask_security import Security, SQLAlchemySessionUserDatastore
from .views.admin import AdminView
from .views.auth import ExtendedLoginForm, LogoutMenuLink
from pathlib import Path
from flask_admin_dashboard.models import db, migrate, User, Role, UserView, RoleView

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
BASE_DIR = Path(__file__).parent.parent.parent.parent.parent.parent.resolve()
BASE_CONFIG_DIR = Path.joinpath(BASE_DIR, 'config')
PACKAGE_DIR = Path(__file__).parent.resolve()
LOGS_DIR = Path.joinpath(BASE_DIR, 'logs')



class AdminDashboard(Admin):

    def __init__(self, app):
        db.app = app
        db.init_app(app)
        migrate.init_app(app, db, render_as_batch=True)
        with app.app_context():
            db.create_all()
        self.security = Security(app, user_datastore, login_form=ExtendedLoginForm)
        super().__init__(app, template_mode='bootstrap3', index_view=AdminView(app_root=app.root_path))
        self.add_category(name='Database')
        self.add_category(name='User Management')
        self.add_view(UserView(User, db.session, category="User Management", name="Users"))
        self.add_view(RoleView(Role, db.session, category="User Management", name="Roles"))
        self.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))

    @staticmethod
    def setup_user():
        role = user_datastore.find_role('SUPER_USER')
        if role is None:
            user_datastore.create_role(name='SUPER_USER', description='Super user access.')
            role = user_datastore.find_role('SUPER_USER')
        user_datastore.create_user(username='will', password="test")
        user = user_datastore.find_user(username='will')
        # role = user_datastore.find_role('SUPER_USER')
        user_datastore.add_role_to_user(user, role)
        db.session.commit()

    @staticmethod
    def initialize_admin():
        if not os.path.exists(LOGS_DIR):
            os.makedirs(LOGS_DIR)
        templates_src = Path.joinpath(Path(PACKAGE_DIR), f'templates')
        templates_dst = Path.joinpath(Path(BASE_DIR), f'templates')
        shutil.copytree(templates_src, templates_dst, symlinks=True, ignore=None, ignore_dangling_symlinks=False,
                        dirs_exist_ok=True)

        static_src = Path.joinpath(Path(PACKAGE_DIR), f'static')
        static_dst = Path.joinpath(Path(BASE_DIR), f'static')
        shutil.copytree(static_src, static_dst, symlinks=True, ignore=None, ignore_dangling_symlinks=False,
                        dirs_exist_ok=True)
