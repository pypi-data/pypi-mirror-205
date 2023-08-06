from pathlib import Path
import operator
import os
from flask_admin import Admin
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_admin_dashboard.models import db, migrate, User, Role, UserView, RoleView
from flask import Blueprint
# from flask_admin_dashboard.views.admin import AdminView
from flask_admin_dashboard.views.auth import ExtendedLoginForm, LogoutMenuLink
from flask_admin import AdminIndexView, expose
from flask_login import login_required

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
admin_dashboard_blueprint = Blueprint(name="admin_dashboard", import_name="admin_dashboard", cli_group="admin", template_folder='templates', static_folder='static')

BASE_DIR = Path(__file__).parent.parent.parent.parent.parent.parent.resolve()
BASE_CONFIG_DIR = Path.joinpath(BASE_DIR, 'config')
PACKAGE_DIR = Path(__file__).parent.resolve()
LOGS_DIR = Path.joinpath(BASE_DIR, 'logs')


@admin_dashboard_blueprint.cli.command('initialize')
def initialize_admin():
    import shutil, os
    import click as click
    from click import prompt
    role = user_datastore.find_role('SUPER_USER')
    if role is None:
        user_datastore.create_role(name='SUPER_USER', description='Super user access.')
        role = user_datastore.find_role('SUPER_USER')

    create_user = prompt("Create New Superuser?", type=click.BOOL)
    if create_user:
        username = prompt("Username", type=click.STRING)
        if user_datastore.find_user(username=username):
            print("User Exists.")
        else:
            pw_match = False
            while not pw_match:
                password = prompt("Password", type=click.STRING, hide_input=False)
                confirm_pw = prompt("Re-Enter Password", type=click.STRING, hide_input=False)
                if password == confirm_pw:
                    user_datastore.create_user(username=username, password=password)
                    user = user_datastore.find_user(username)
                    user_datastore.add_role_to_user(user, role)
                    db.session.commit()
                else:
                    print("Password did not match.")

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



class AdminView(AdminIndexView):

    def __init__(self, app_root=None):
        super().__init__()
        self.app_root = app_root

    @login_required
    @expose('/')
    def index(self):
        logs = []
        print(f"{self.app_root}/logs/")
        log_files = os.listdir(f"{self.app_root}/logs/")
        index = 0
        for file in log_files:
            index += 1
            this_file = {"name": file.lower(), "index": index}
            with open(f"{self.app_root}/logs/{file}", "r", encoding="utf-8") as f:
                this_file["content"] = f.read()
            logs.append(this_file)
        logs.sort(key=operator.itemgetter('name'))

        for log in logs:
            print(log.get('name'))
        return self.render('admin/logs.html', logs=logs)




class AdminDashboard(Admin):
    def __init__(self, app):
        db.app = app
        db.init_app(app)
        app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True
        migrate.init_app(app, db, render_as_batch=True)
        with app.app_context():
            db.create_all()
            app.register_blueprint(admin_dashboard_blueprint)

        self.security = Security(app, user_datastore, login_form=ExtendedLoginForm)
        super().__init__(app, template_mode='bootstrap3',  index_view=AdminView(app_root=app.root_path))
        self.add_category(name='Database')
        self.add_category(name='User Management')
        self.add_view(UserView(User, db.session, category="User Management", name="Users"))
        self.add_view(RoleView(Role, db.session, category="User Management", name="Roles"))
        self.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))




