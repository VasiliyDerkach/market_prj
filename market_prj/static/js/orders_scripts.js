window.onload = function () {
    $('.td4 order formset_td').on('click','input[type="number"]', function () {
        var t_href = event.target;

        $.ajax({
            url: "/ordersapp/edit_accommodation/" + t_href.value ,

            success: function (data) {
                $('.orderitem_list').html(data.result);
            },
        });
//
        event.preventDefault();
    });
}
