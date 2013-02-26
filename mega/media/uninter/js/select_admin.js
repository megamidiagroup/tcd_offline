$(function() {

    $('#action-toggle').click(function(e) {
        var obj   = $(this);
        var count = 0;
        $('.action-select').each(function(e) {
            if ( obj.is(':checked') ) {
                $(this).attr("checked", true);
                count++;
            } else {
                $(this).attr("checked", false);
            }
        });
        $('.action-counter').html(count + ' de ' + _actions_icnt + ' selecionados');
    });

    $('.action-select').click(function(e) {
        var obj   = $(this);
        var count = 0;
        $('.action-select:checked').each(function(e) {
            count++;
        });
        if ( obj.is(':checked') && count == parseInt(_actions_icnt) ) {
            $('#action-toggle').attr("checked", true);
        } else {
            $('#action-toggle').attr("checked", false);
        }
        $('.action-counter').html(count + ' de ' + _actions_icnt + ' selecionados');
    });

    $('.button').click(function(e){
        var count = 0;
        if( $('select[name=action]').val() == '' )
        {
            alert('Selecione uma ação.');
        } else {
            $('.action-select:checked').each(function(e) {
                count++;
            });
            if ( count > 0 )
            {
                $('form').submit();
            } else {
                alert('Selecione pelo menos um item da lista.');
            }
        }
    });

});
