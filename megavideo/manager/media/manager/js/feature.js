//para bloquear bottons para depois desbloquear;

var channel = "";

function init(){
	
	if($(".channel").length && $(".channel").html() != "") channel = $(".channel").html();

    // do exclude with redirection
    $('.exclude').click(function(e){

        $('#confirm').attr('url', $(this).attr('url')).attr('target_id', $(this).attr('target_id'));

           confirm($(this).attr('msg'));

        return false;

    });

    if ($('#confirm').length > 0) {
        $('#confirm').jqm({
            overlay: 80,
            trigger: false
        });
    }

    //monta menu
    montaMenu();
    
    try {
		$(".ddselect").css("z-index", "10000").msDropDown({visibleRows:15, rowHeight:23});
		$(".ddTitle span.arrow").before('<span class="before"><img src="/megavideo/static/manager/images/combo1.png" border="0" /></span>');
		$(".ddTitle span.arrow").after('<span class="after"><img src="/megavideo/static/manager/images/combo3.png" border="0" /></span>');
	} catch(e) {
		alert("Error msDropDown: " + e);
	} 

}

function montaMenu(){

    $("img.bt_deletar").click(function(e){

        var url        = channel + "manager/featured/ajaxdel/";
        var category_id = $(this).attr("name");

        $.post(url, { id: category_id },
            function(data){
                if (data.status == true) {

                    $('div#blockCategory').load(channel + 'manager/featured/ajaxlistcategory/', {}, function(e){
                        montaMenu();
                    });

                } else {

                    alert("erro em deletar uma categoria!");

                }
            }, 'json');

    });

    /* invoca combo */
    $("input.category").each(function(e){
        $(this).attr("class", "category" + $(this).attr("name"));
        $("input.category" + $(this).attr("name")).mcDropdown("#categorymenu" + $(this).attr("name"), {delim: " : ", allowParentSelect : false, select:function() { returnValue() } });
    });

}

/* importante para a plugin jquery */
function returnValue() {

    var itensCategory = new Array();
    var url           = channel + "manager/featured/ajaxadd/";

    $("input.itensCategory").each(function(e){

        var verifica = true;
        var valor    = $(this).val();

        for (var u in itensCategory){
            if (itensCategory[u] == valor){
                verifica = false;
            }
        }

        if (valor != "0" && valor != "" && verifica == true){
            itensCategory.push($(this).val());
        }

    });

    $.post(url, { itens: itensCategory, typevideofeatured: 'c' },
        function(data){
            if (data.status == true) {

                $('div#blockCategory').load(channel + 'manager/featured/ajaxlistcategory/', {}, function(e){
                    montaMenu();
                });

            } else {

                alert("erro em deletar uma categoria!");

            }
        }, 'json');

}

/* para adicionar video para destaque */
function addVideo(video_id, url) {

    var itensCategory = new Array();
    url_redirect = url + 'manager/featured/'
    url += "manager/featured/ajaxadd/";
	
    itensCategory.push(video_id);

    $.post(url, { itens: itensCategory, typevideofeatured: 'v' },
        function(data){
            if (data.status == true) {

                window.document.location = url_redirect ;

            } else {

                alert("erro para salvar o video de destaque!");

            }
        }, 'json');

}

/** functions system **/
function msg( alvo, msg, type, block ) {

    switch ( type ) {

        case "error":
        case "erro":
            $("#" + alvo).css("color", "#D71009");
            $("#" + alvo).css("height", "25px");
            $("#" + alvo).html(msg);
        break;

        case "block":
            $("#" + alvo).css("color", "#D71009");
            $("#" + alvo).css("height", "25px");
            for (var i in block){
                $("#" + block[i]).css("display", "none");
                btnsBlocked = [block[i]];
            }
            $("#" + alvo).html(msg);
        break;

        default:
            for (var i in btnsBlocked){
                $("#" + btnsBlocked[i]).css("display", "block");
                btnsBlocked = '';
            }
            $("#" + alvo).css("color", "#06B806");
            $("#" + alvo).html(msg);
        break;

    }

    $('img').css("margin-right", "3px");

}

function confirm(msg, callback) {

    $('#confirm').jqmShow().find('p.jqmConfirmMsg').html(msg).end();
    $('table td.sim:visible, table td.no:visible').unbind('click');
    $('table td.sim:visible, table td.no:visible').bind('click', function(e){

        if(this.id == "1"){

            var id  = $('#confirm').attr('target_id');
            var url = $('#confirm').attr('url');

            $.post(url + 'ajaxdel/', { id: id },
              function(data){
                if ( data.status == true ){
                    window.document.location = url;
                }else{
                    alert('Error ao excluir a informação');
                }
              }, 'json');

        }

        $('#confirm').jqmHide();

    });

}

function selectionCategory(item){
    window.document.location = $(item).attr("class") + item.value;
}

$(document).ready(init);
