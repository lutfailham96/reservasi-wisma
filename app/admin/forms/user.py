from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, EqualTo


class UserForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = StringField(validators=[EqualTo('password_confirmation')])
    password_confirmation = StringField(validators=[EqualTo('password')])
    nama = StringField(validators=[DataRequired()])
    jabatan = StringField(validators=[DataRequired()])
    status = StringField(validators=[DataRequired()])


class UserDelForm(FlaskForm):
    id_user = StringField(validators=[DataRequired()])


class UserProfileForm(FlaskForm):
    nama = StringField(validators=[DataRequired])
    password = StringField(validators=[EqualTo('password_confirmation')])
    password_confirmation = StringField(validators=[EqualTo('password')])
