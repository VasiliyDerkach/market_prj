window.onload = function () {
    $('.orderitem_list').on('submit','div[name="accommodation_order"]', function () {
        var t_href = event.target;
        print('accommodation_order',t_href.value)

//        $.ajax({
//            url: "/ordersapp/edit_night/" + t_href.name ,
//
//            success: function (data) {
//                $('.orderitem_list').html(data.result);
//            },
//        });
//
//        event.preventDefault();
    });
}
