window.onload = function () {
    $('.order_form').on('click','input[name^="orderitems-"]', function () {
        var t_href = event.target;
        var vlu = t_href.value;
        var exs= $('#id_order_exist').value();
        if (vlu) {
            var vlu = 'vlu'
        }
        else {
            var vlu = 'none'
        }
        $.ajax({
            url: "/order/edit_accommodation/" + exs + '/' + t_href.name+'/'+t_href.value+'/' ,

            success: function (data) {
                $('.order_form').html(data.result);
            },
        });
//
        event.preventDefault();
    });
    $('.order_form').on('change','select[name^="orderitems-"]', function () {
        var t_href = event.target;
        var vlu = t_href.value;
        var exs= $('#id_order_exist').value();
        if (vlu) {
            var vlu = vlu
        }
        else {
            var vlu = 'none'
        }
        $.ajax({
            url: "/order/edit_accommodation/" + exs + '/' + t_href.name+'/'+vlu+'/' ,

            success: function (data) {
                $('.order_form').html(data.result);
            },
        });
//
        event.preventDefault();
    });
}
