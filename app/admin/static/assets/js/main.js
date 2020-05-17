$(document).ready(function () {
    $('.sidebar-menu').tree();
    init_data_table();
});

// init data table
function init_data_table() {
    $('#table_user').DataTable();
    $('#table_kamar').DataTable();
    // $('#table_kelas_kamar').DataTable({
    //     'ajax': '/api/kelas_kamar'
    // });
    $('#table_kelas_kamar').DataTable();
    $('#table_transaksi').DataTable();
    $('#table_wisma').DataTable();
    mask_currency();
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
            refresh_table('kelas_kamar');
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
                // show_data_table(type)
                $('#row-' + id).remove();
                init_data_table();
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
