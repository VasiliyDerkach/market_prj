window.onload = function () {
    $('.order_form').on('click','input[name^="orderitems-"]', function () {
        var t_href = event.target;
        var vlu = t_href.value;
//        извлечь номер строки из t_href
        var idx = t_href.name.replace('orderitems-','');
        var idx = idx.slice(0,idx.indexOf('-'));
        var exs= $('#id_orderitems-'+idx+'-id').attr('value');
        if (exs) {
            var exs = exs;
        }
        else {
            var exs = '-';
        };
        if (vlu) {
            var vlu = vlu;
        }
        else {
            var vlu = 'none';
        };
        $.ajax({
            url: "/order/edit_accommodation/" + exs + '/' + t_href.name+'/'+vlu+'/' ,

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
        var idx = t_href.name.replace('orderitems-','');
        var idx = idx.slice(0,idx.indexOf('-'));
        var exs= $('#id_orderitems-'+idx+'-id').attr('value');
        if (exs) {
            var exs = exs;
        }
        else {
            var exs = '-';
        };
        if (vlu) {
            var vlu = vlu;
        }
        else {
            var vlu = 'none';
        };
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
