from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class KelasKamarForm(FlaskForm):
    nama_kelas = StringField(validators=[DataRequired()])
    id_wisma = StringField(validators=[DataRequired()])
    harga_kelas = StringField(validators=[DataRequired()])


class KamarForm(FlaskForm):
    nama_kamar = StringField(validators=[DataRequired()])
    id_kelas_kamar = StringField(validators=[DataRequired()])
    kondisi = StringField(validators=[DataRequired()])
