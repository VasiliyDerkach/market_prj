window.onload = function () {
    $('.orderitem_list').on('select','select[name="orderitems-0-accommodation"]', function () {
        var t_href = event.target;

        $.ajax({
            url: "/ordersapp/edit_accommodation/" + t_href.value ,
//
//            success: function (data) {
//                $('.orderitem_list').html(data.result);
//            },
        });
//
        event.preventDefault();
    });
}
