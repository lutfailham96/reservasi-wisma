$(document).ready(function () {
    $('.sidebar-menu').tree();
    init_data_table();
});

// init data table
function init_data_table() {
    $('#table_user').DataTable();
    $('#table_kamar').DataTable();
    //$('#table_kelas_kamar').DataTable();
    $('#table_transaksi').DataTable();
    $('#table_wisma').DataTable();
    // $('#table_kelas_kamar').DataTable({
    //     'ajax': '/api/kelas_kamar'
    // });
    // mask_currency();
    $('#table_kelas_kamar').DataTable( {
        "processing": true,
        "serverSide": true,
        "ajax": $.fn.dataTable.pipeline( {
            url: '/admin/ajax/kelas_kamar',
            pages: 5 // number of pages to cache
        } ),
        'columns': [
            { data: 'index'},
            { data: 'nama_kelas'},
            { data: 'id_wisma'},
            { data: 'harga_kelas' },
            {
                data: null,
                render: function (data, type, row) {
                    return '<button class="btn btn-danger">Tombol</button><button class="btn btn-danger">Hapus</button>'
                }
            }
        ]
    } );
}

// mask currency column
function mask_currency() {
    const uang = $('.uang')
    uang.mask('000.000.000', {reverse: true});
    uang.prepend('Rp. ');
}

// show confirmation
function delete_confirmation(type, id) {
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
            delete_data(type, id)
        } else {
            show_notification('error', 'Gagal menghapus data')
        }
    })
}

// delete data
function delete_data(type, id) {
    let data = {
        'id': id
    }

    $.ajax({
        async: true,
        url: '/admin/ajax/' + type,
        method: 'DELETE',
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        data: JSON.stringify(data),
        // beforeSend: before_wisma(),
        success: function(data, status, xhr) {
            if (xhr.status === 204) {
                show_notification('success', 'Data berhasil dihapus');
                $('#table_' + type).DataTable().ajax.reload()
                $('#row-' + id).remove();
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

function refresh_table(table) {
    let select = $('#table_' + table)
    // select.DataTable({
    //     'ajax': '/api/kelas_kamar'
    // })
    // select.ajax.reload(fun);
}

// function show_data_table(type) {
//     $.ajax({
//         async: true,
//         url: '/api/' + type,
//         method: 'GET',
//         dataType: 'json',
//         success: function(data, status, xhr) {
//             let row = data['data']
//             let html = '';
//             for (let i=0; i<row.length; i++) {
//                 html += row[i]
//                 // html += '<tr>'+
//                 //     '<td>' + (i + 1) +'</td>' +
//                 //     '<td>' + row[i].nama_kelas +'</td>' +
//                 //     '<td>' + row[i].nama_wisma +'</td>' +
//                 //     '<td class="uang">' + row[i].harga_kelas +'</td>' +
//                 //     '<td class="text-center" style="width: 150px">' +
//                 //         '<a href="/admin/home/kelas_kamar/edit/' + row[i].id + '" class="btn bg-purple btn-sm"><i class="fa fa-pencil"></i>Update</a>' +
//                 //         '<button onclick="delete_confirmation('+ type +', ' + row[i].id + ')" class="btn btn-danger btn-sm"><i class="fa fa-trash">Hapus</i></button>' +
//                 //     '</td>'
//             }
//             $('#table_kelas_kamar tbody').html(html);
//         }
//     });

$.fn.dataTable.pipeline = function ( opts ) {
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

        if ( settings.clearCache ) {
            ajax = true;
            settings.clearCache = false;
        }
        else if ( cacheLower < 0 || requestStart < cacheLower || requestEnd > cacheUpper ) {
            ajax = true;
        }
        else if ( JSON.stringify( request.order )   !== JSON.stringify( cacheLastRequest.order ) ||
            JSON.stringify( request.columns ) !== JSON.stringify( cacheLastRequest.columns ) ||
            JSON.stringify( request.search )  !== JSON.stringify( cacheLastRequest.search )
        ) {
            ajax = true;
        }

        cacheLastRequest = $.extend( true, {}, request );
        if ( ajax ) {
            if ( requestStart < cacheLower ) {
                requestStart = requestStart - (requestLength*(conf.pages-1));
                if ( requestStart < 0 ) {
                    requestStart = 0;
                }
            }
            cacheLower = requestStart;
            cacheUpper = requestStart + (requestLength * conf.pages);
            request.start = requestStart;
            request.length = requestLength*conf.pages;
            if ( typeof conf.data === 'function' ) {
                let d = conf.data( request );
                if ( d ) {
                    $.extend( request, d );
                }
            }
            else if ( $.isPlainObject( conf.data ) ) {
                $.extend( request, conf.data );
            }

            return $.ajax( {
                "type":     conf.method,
                "url":      conf.url,
                "data":     request,
                "dataType": "json",
                "cache":    false,
                "success":  function ( json ) {
                    cacheLastJson = $.extend(true, {}, json);

                    if ( cacheLower !== drawStart ) {
                        json.data.splice( 0, drawStart-cacheLower );
                    }
                    if ( requestLength >= -1 ) {
                        json.data.splice( requestLength, json.data.length );
                    }

                    drawCallback( json );
                }
            } );
        }
        else {
            json = $.extend( true, {}, cacheLastJson );
            json.draw = request.draw; // Update the echo for each response
            json.data.splice( 0, requestStart-cacheLower );
            json.data.splice( requestLength, json.data.length );

            drawCallback(json);
        }
    }
};

// Register an API method that will empty the pipelined data, forcing an Ajax
// fetch on the next draw (i.e. `table.clearPipeline().draw()`)
$.fn.dataTable.Api.register( 'clearPipeline()', function () {
    return this.iterator( 'table', function ( settings ) {
        settings.clearCache = true;
    } );
} );