from flask_security import UserMixin, RoleMixin, current_user, utils, roles_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

# from flask_login.utils import current_user

db = SQLAlchemy()
migrate = Migrate()

# AUTH

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # email = db.Column('email', db.String(255), unique=True)
    username = db.Column('username', db.String(255))
    password = db.Column(db.String(255))
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))


class UserView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    column_searchable_list = ["username"]
    page_size = 10

    def is_accessible(self):
        return current_user.is_authenticated

    @event.listens_for(User.password, 'set', retval=True)
    def hash_user_password(target, value, oldvalue, initiator):
        if value != oldvalue:
            return utils.hash_password(value)
        return value


class RoleView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    page_size = 10

    def is_accessible(self):
        return current_user.is_authenticated


class RoleUsersView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    page_size = 10

    def is_accessible(self):
        return current_user.is_authenticated
