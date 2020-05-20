$(document).ready(function () {
    $('.sidebar-menu').tree();
    init_data_table();
    mask_rupiah();
});

// init data table
function init_data_table() {
    $('#table_user').DataTable({
        'processing': true,
        'serverSide': true,
        'ajax': $.fn.dataTable.pipeline({
            url: '/admin/ajax/data/user',
            pages: 5
        }),
        'columns': [
            { data: 'index' },
            { data: 'nama' },
            { data: 'username' },
            {
                data: null,
                render: function (data) {
                    if (data['jabatan'] === 0) {
                        return 'Admin'
                    } else {
                        return 'Operator'
                    }
                }
            },
            {
                data: null,
                render: function (data) {
                    if (data['status'] === 1) {
                        return '<span class="label bg-green">Aktif</span>'
                    } else {
                        return '<span class="label bg-red">Nonaktif</span>'
                    }
                }
            },
            {
                data: null,
                render: function (data) {
                    return '<a href="/admin/home/user/edit/' + data['id'] + '" class="btn bg-purple btn-sm"><i class="fa fa-pencil"></i>Update </a> <button onclick="delete_confirmation(\'user\', ' + data['id'] + ')" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i>Hapus</button>'
                }
            }
        ],
        'columnDefs': [
            { className: "text-center", targets: 5 },
            { className: "action-button", targets: 5 },
        ],
    });
    $('#table_kamar').DataTable({
        'processing': true,
        'serverSide': true,
        'ajax': $.fn.dataTable.pipeline({
            url: '/admin/ajax/data/kamar',
            pages: 5
        }),
        'columns': [
            { data: 'index' },
            { data: 'nama_kamar' },
            { data: 'nama_kelas' },
            {
                data: null,
                render: function (data) {
                    if (data['kondisi'] === 0) {
                        return '<span class="label bg-green">Kosong</span>'
                    } else if (data['kondisi'] === 1) {
                        return '<span class="label bg-yellow">Dibooking</span>'
                    } else if (data['kondisi'] === 2) {
                        return '<span class="label bg-gray">Kotor</span>'
                    } else if (data['kondisi'] === 3) {
                        return '<span class="label bg-red">Rusak</span>'
                    }
                }
            },
            {
                data: 'harga_kelas',
                render: $.fn.DataTable.render.number('.', ',', 0, 'Rp ')
            },
            {
                data: null,
                render: function (data) {
                    return '<a href="/admin/home/kamar/edit/' + data['id'] + '" class="btn bg-purple btn-sm"><i class="fa fa-pencil"></i>Update </a> <button onclick="delete_confirmation(\'kamar\', ' + data['id'] + ')" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i>Hapus</button>'
                }
            }
        ],
        'columnDefs': [
            { className: "text-center", targets: 5 },
            { className: "action-button", targets: 5 },
        ],
    });
    $('#table_transaksi').DataTable();
    $('#table_wisma').DataTable({
        'processing': true,
        'serverSide': true,
        'ajax': $.fn.dataTable.pipeline({
            url: '/admin/ajax/data/wisma',
            pages: 5
        }),
        'columns': [
            { data: 'index' },
            { data: 'nama_wisma' },
            { data: 'alamat_wisma' },
            { data: 'no_telp' },
            {
                data: null,
                render: function (data) {
                    return '<a href="/admin/home/wisma/edit/' + data['id'] + '" class="btn bg-purple btn-sm"><i class="fa fa-pencil"></i>Update </a> <button onclick="delete_confirmation(\'wisma\', ' + data['id'] + ')" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i>Hapus</button>'
                }
            }
        ],
        'columnDefs': [
            { className: "text-center", targets: 4 },
            { className: "action-button", targets: 4 },
        ],
    });
    $('#table_kelas_kamar').DataTable( {
        'processing': true,
        'serverSide': true,
        'ajax': $.fn.dataTable.pipeline({
            url: '/admin/ajax/data/kelas_kamar',
            pages: 5
        }),
        'columns': [
            { data: 'index' },
            { data: 'nama_kelas' },
            { data: 'nama_wisma' },
            {
                data: 'harga_kelas',
                render: $.fn.DataTable.render.number('.', ',', 0, 'Rp ')
            },
            {
                data: null,
                render: function (data) {
                    return '<a href="/admin/home/kelas_kamar/edit/' + data['id'] + '" class="btn bg-purple btn-sm"><i class="fa fa-pencil"></i>Update </a> <button onclick="delete_confirmation(\'kelas_kamar\', ' + data['id'] + ')" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i>Hapus</button>'
                }
            }
        ],
        'columnDefs': [
            { className: "text-center", targets: 4 },
            { className: "action-button", targets: 4 }
        ],
    });
}

// pipeline datatable
$.fn.dataTable.pipeline = function (opts) {
    let conf = $.extend({
        pages: 5,
        url: '',
        data: null,
        method: 'GET'
    }, opts );
    let cacheLower = -1;
    let cacheUpper = null;
    let cacheLastRequest = null;
    let cacheLastJson = null;
    return function (request, drawCallback, settings) {
        let ajax = false;
        let requestStart = request.start;
        let drawStart = request.start;
        let requestLength = request.length;
        let requestEnd = requestStart + requestLength;
        if (settings.clearCache) {
            ajax = true;
            settings.clearCache = false;
        }
        else if (cacheLower < 0 || requestStart < cacheLower || requestEnd > cacheUpper) {
            ajax = true;
        }
        else if (JSON.stringify(request.order) !== JSON.stringify(cacheLastRequest.order) ||
            JSON.stringify(request.columns) !== JSON.stringify(cacheLastRequest.columns) ||
            JSON.stringify(request.search) !== JSON.stringify(cacheLastRequest.search)
        ) {
            ajax = true;
        }
        cacheLastRequest = $.extend(true, {}, request);
        if (ajax) {
            if (requestStart < cacheLower) {
                requestStart = requestStart - (requestLength*(conf.pages-1));
                if (requestStart < 0) {
                    requestStart = 0;
                }
            }
            cacheLower = requestStart;
            cacheUpper = requestStart + (requestLength * conf.pages);
            request.start = requestStart;
            request.length = requestLength*conf.pages;
            if (typeof conf.data === 'function') {
                let d = conf.data(request);
                if (d) {
                    $.extend(request, d);
                }
            }
            else if ($.isPlainObject(conf.data)) {
                $.extend(request, conf.data);
            }
            return $.ajax({
                'type': conf.method,
                'url': conf.url,
                'data': request,
                'dataType': 'json',
                'cache': false,
                'success': function (json) {
                    cacheLastJson = $.extend(true, {}, json);
                    if (cacheLower !== drawStart) {
                        json.data.splice(0, drawStart-cacheLower);
                    }
                    if (requestLength >= -1) {
                        json.data.splice(requestLength, json.data.length);
                    }
                    drawCallback(json);
                }
            });
        }
        else {
            let json = $.extend(true, {}, cacheLastJson);
            json.draw = request.draw;
            json.data.splice(0, requestStart-cacheLower);
            json.data.splice(requestLength, json.data.length);
            drawCallback(json);
        }
    }
};

// clear pipeline datatable
$.fn.dataTable.Api.register('clearPipeline()', function () {
    return this.iterator('table', function (settings) {
        settings.clearCache = true;
    });
});

// mask currency
function mask_rupiah() {
    $('.mata-uang').mask('0.000.000.000', { 'reverse': true });
}

// show confirmation
function delete_confirmation(table_name, id) {
    Swal.fire({
        title: 'Apa anda yakin ingin menghapus data?',
        text: "Perubahan data tidak dapat dikembalikan!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        cancelButtonText: 'Batal',
        confirmButtonText: 'Ya'
    }).then((result) => {
        if (result.value) {
            delete_data(table_name, id)
        }
    })
}

// delete data
function delete_data(table_name, id) {
    let data = {
        'id': id
    }
    $.ajax({
        async: true,
        url: '/admin/ajax/data/' + table_name,
        method: 'DELETE',
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        data: JSON.stringify(data),
        // beforeSend: ,
        success: function(data, status, xhr) {
            if (xhr.status === 204) {
                show_notification('success', 'Data berhasil dihapus');
                $('#table_' + table_name).DataTable().clearPipeline().draw();
            }
            else {
                show_notification('error', 'Gagal menghapus data');
            }
        }
    });
}

// notification toaster
function show_notification(status, msg) {
    toastr.options = {
        'closeButton': false,
        'debug': false,
        'newestOnTop': true,
        'progressBar': false,
        'positionClass': 'toast-top-right',
        'preventDuplicates': false,
        'onclick': null,
        'showDuration': '300',
        'hideDuration': '1000',
        'timeOut': '5000',
        'extendedTimeOut': '1000',
        'showEasing': 'swing',
        'hideEasing': 'linear',
        'showMethod': 'fadeIn',
        'hideMethod': 'fadeOut'
    }
    if (status === 'success') {
        toastr['success'](msg, 'Sukses')
    } else {
        toastr['error'](msg, 'Gagal')
    }
}