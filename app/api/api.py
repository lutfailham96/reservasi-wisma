from flask import Blueprint, request, jsonify, abort, url_for, render_template

from app.admin.databases.models.kamar import KelasKamar, Kamar
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


# @bp_api.route('/test')
# def test():
#     data = {
#         'data': [
#             [
#                 "Tiger Nixon"
#             ]
#         ]
#     }
#     return jsonify(data)


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

@bp_api.route('/test')
def test():
    return render_template('test.html')


@bp_api.route('/ajax/test')
def ajax_test():
    draw = int(request.args.get('draw'))
    per_page = int(request.args.get('length'))
    page = round((int(request.args.get('start')) / per_page) + 1)
    search_arg = request.args.get('search[value]')
    search = "%{}%".format(search_arg)

    kamars = Kamar.query.paginate(page, per_page, False)

    if len(str(search_arg).strip()) > 0:
        # kamars = Kamar.query.filter((Kamar.nama_kamar.like(search))).all()
        kamars = Kamar.query.filter(Kamar.nama_kamar.like(search)).paginate(page, per_page, False)

    total_count = db_sql.session.query(Kamar).count()
    filter_count = kamars.total

    cols = []
    for index, kamar in enumerate(kamars.items):
        row = {
            'index': index + 1,
            'nama_kamar': kamar.nama_kamar,
            'id_kelas_kamar': kamar.id_kelas_kamar,
            'kondisi': kamar.kondisi
        }
        cols.append(row)

    data = {
        "draw": draw,
        "recordsTotal": total_count,
        "recordsFiltered": filter_count,
        "data": cols
    }

    return data


@bp_api.route('/hell')
def hell():
    dataset = db_sql.session.query(KelasKamar, Wisma).join(Wisma, KelasKamar.id_wisma == Wisma.id) \
        .order_by(Wisma.nama_wisma, KelasKamar.nama_kelas).paginate(1, 20, False)
    print(dataset.total)
    return ''
