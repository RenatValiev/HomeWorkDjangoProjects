function checkDeleteAdvert(id) {
    let text = "Are you sure you want to delete the advert?";
    if (confirm(text)) {
        window.location.replace('/adverts/' + id + '/delete/')
    }
}

$('#myModal').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
})