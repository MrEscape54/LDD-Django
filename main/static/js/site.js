$(document).on('click', '.confirm-delete', function () {
    $("#confirmDeleteModal").attr("caller-id", $(this).attr("id"));
    $('#deleteForm').attr('action', '/address/' + $("#confirmDeleteModal").attr("caller-id") + '/delete/')

    $("#confirmDeleteModal").attr("caller-address", $(this).attr('js-address'));
    $('.modal-body').text('¿Está seguro de eliminar la dirección ' + $("#confirmDeleteModal").attr("caller-address") + '?')
});

