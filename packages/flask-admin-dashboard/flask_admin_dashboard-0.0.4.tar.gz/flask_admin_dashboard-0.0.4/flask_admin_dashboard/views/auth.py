from flask import Blueprint, render_template, request, redirect, url_for, Flask, flash
from flask_admin import BaseView, expose
from flask_admin.menu import MenuLink
from flask_login import login_required
from flask_security import current_user, LoginForm
import flask_security
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, BooleanField, Form, DateTimeField, TextAreaField, FieldList, \
    FormField, SubmitField
from wtforms.validators import InputRequired
from datetime import datetime

from ..utilities.jsonhandler import JSONReader

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/logout')
def logout():
    flask_security.logout_user()
    return redirect(url_for('index'))


class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated


class ExtendedLoginForm(LoginForm):
    email = StringField('Username')
    password = PasswordField('Password')
    remember = BooleanField('Remember Me')


class TokenView(BaseView):
    json_handler = JSONReader()

    def __init__(self, clients, **kwargs):
        super().__init__(**kwargs)
        self.clients = clients

    @login_required
    @expose('/', methods=["GET", "POST"])
    def index(self):
        token_data = self.get_token_data()
        form = TokenForm(token_data=token_data)
        if request.method == "POST":
            updated_client_name = ""
            updated_auth = {}
            for item in form.data.get("token_data"):
                if item.get("update"):
                    updated_client_name = item.get("app_name")
                    updated_auth = item
            for client in self.clients:
                if client.name == updated_client_name:
                    client.update_authorization(authorization_data={
                        'access_token': updated_auth.get("access_token"),
                        'refresh_token': updated_auth.get("refresh_token"),
                        'expires_at': updated_auth.get("expires_at")
                    }, fix_time=True)
            return redirect(request.referrer)
        return self.render('admin/tokens.html', token_data=token_data, form=form)

    def get_token_data(self):
        authorizations = []

        for client in self.clients:
            client_auth = client.auth_handler.get_authorization()
            update_time = JSONReader.extract_value(client_auth, "updated_at")
            expires_time = JSONReader.extract_value(client_auth, "expiration_datetime")

            if update_time:
                updated_at = datetime.fromtimestamp(update_time)
            else:
                updated_at = 'None'
            if expires_time and type(expires_time) == int:
                expires_at = datetime.fromtimestamp(expires_time)
            elif expires_time and type(expires_time) == float:
                expires_at = datetime.fromtimestamp(int(expires_time))
            elif expires_time and type(expires_time) == str:
                expires_at = expires_time
            else:
                expires_at = 'None'

            new_item = {
                "app_name": client.name,
                "access_token": JSONReader.extract_value(client_auth, "access_token") or 'None',
                "refresh_token": JSONReader.extract_value(client_auth, "refresh_token") or 'None',
                "updated_at": updated_at,
                "expires_at": expires_at,
            }

            authorizations.append(new_item)
        return authorizations


class TokenEntryForm(FlaskForm):
    app_name = StringField('app_name')
    access_token = StringField('access token')
    refresh_token = StringField('refresh token')
    updated_at = StringField('updated at')
    expires_at = StringField('expires at')
    update = SubmitField('Update')


class TokenForm(FlaskForm):
    token_data = FieldList(FormField(TokenEntryForm), min_entries=1)
