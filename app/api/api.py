from flask import Blueprint, request, jsonify, abort, url_for

from app.admin.databases.models.kamar import KelasKamar
from app.admin.databases.models.wisma import Wisma
from app.databases import db_sql
from app.managers import csrf

bp_api = Blueprint('api', __name__, static_folder='static', template_folder='templates')


@bp_api.route('/kelas', methods=['POST'])
@csrf.exempt
def api_kelas():
    id_wisma = request.form.get('id_wisma')
    kelas_kamars = KelasKamar.query.filter_by(id_wisma=id_wisma).order_by(KelasKamar.nama_kelas)
    if kelas_kamars is not None:
        data = [data.to_dict() for data in kelas_kamars]
        return jsonify(data)
    return 'None', 404


@bp_api.route('/test')
def test():
    data = {
        'data': [
            [
                "Tiger Nixon"
            ]
        ]
    }
    return jsonify(data)


@bp_api.route('/kelas_kamar', methods=['GET', 'DELETE'])
@csrf.exempt
def kelas_kamar():
    if request.method == 'DELETE':
        id_data = request.get_json()['id']
        if KelasKamar.delete(id_data):
            return {
                'success': True
            }, 204
        abort(500)
    all_data = db_sql.session.query(KelasKamar, Wisma).join(Wisma, KelasKamar.id_wisma == Wisma.id).order_by(Wisma.nama_wisma, KelasKamar.nama_kelas)
    data = []
    for index, single_data in enumerate(all_data):
        row = [
            index + 1,
            single_data[1].nama_wisma,
            single_data[0].nama_kelas,
            single_data[0].harga_kelas,
            '<a href="{}" class="btn bg-purple btn-sm"><i class="fa fa-pencil"></i>Update</a>'
            '<button onclick="delete_confirmation({}, {})" class="btn btn-danger btn-sm">'
            '<i class="fa fa-trash"></i>Hapus</button>'.format(url_for('admin.kelas_kamar_edit', id_kelas_kamar=single_data[0].id), '\'kelas_kamar\'', single_data[0].id)
        ]
        data.append(row)
    return {
        'success': True,
        'data': data
    }

# @bp_api.route('/kelas_kamar', methods=['GET', 'DELETE'])
# @csrf.exempt
# def kelas_kamar():
#     if request.method == 'DELETE':
#         id_data = request.get_json()['id']
#         if KelasKamar.delete(id_data):
#             return {
#                        'success': True
#                    }, 204
#         abort(500)
#     all_data = db_sql.session.query(KelasKamar, Wisma).join(Wisma, KelasKamar.id_wisma == Wisma.id)\
#         .order_by(Wisma.nama_wisma, KelasKamar.nama_kelas)
#     data = []
#     for index, single_data in enumerate(all_data):
#         row = '<tr id="row-{}">' \
#                 '<td>{}</td>' \
#                 '<td>{}</td>' \
#                 '<td>{}</td>' \
#                 '<td>{}</td>' \
#                 '<td>' \
#                 '<a href="{}" class="btn bg-purple btn-sm"><i class="fa fa-pencil"></i>Update</a>' \
#                 '<button onclick="delete_confirmation({}, {})" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i>Hapus</button>'\
#                 '</td>' \
#               '</tr>'.format(single_data[0].id, index + 1, single_data[0].nama_kelas, single_data[1].nama_wisma, single_data[0].harga_kelas, url_for('admin.kelas_kamar_edit', id_kelas_kamar=single_data[0].id), "\'kelas_kamar\'", single_data[0].id)
#         data.append(row)
#     return {
#         'success': True,
#         'data': data
#     }
