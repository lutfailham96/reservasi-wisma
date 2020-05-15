from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class TransaksiForm(FlaskForm):
    nama_konsumen = StringField(validators=[DataRequired()])
    alamat_konsumen = StringField(validators=[DataRequired()])
    kontak_konsumen = StringField(validators=[DataRequired()])
    id_kelas = IntegerField(validators=[DataRequired()])
    tanggal = StringField(validators=[DataRequired()])
