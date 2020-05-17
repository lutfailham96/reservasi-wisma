from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class WismaForm(FlaskForm):
    nama_wisma = StringField(validators=[DataRequired()])
    alamat_wisma = StringField(validators=[DataRequired()])
    no_telp = StringField(validators=[DataRequired()])


class WismaDelForm(FlaskForm):
    id_wisma = StringField(validators=[DataRequired()])
