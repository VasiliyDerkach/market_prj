window.onload = function () {
    $('.order_form').on('click','input[type="number"]', function () {
        var t_href = event.target;

        $.ajax({
            url: "/order/edit_accommodation/" + t_href.name+'/'+t_href.value+'/' ,

            success: function (data) {
                $('.order_form').html(data.result);
            },
        });
//
        event.preventDefault();
    });
}
