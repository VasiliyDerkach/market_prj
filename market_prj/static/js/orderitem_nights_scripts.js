window.onload = function () {
    $('.orderitem_list').on('click','input[type="number_order_nights"]', function () {
        var t_href = event.target;

        $.ajax({
            url: "/ordersapp/edit_night/" + t_href.name ,

            success: function (data) {
                $('.orderitem_list').html(data.result);
            },
        });

        event.preventDefault();
    });
}
