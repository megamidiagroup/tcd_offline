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

    $('.exclude_comment').click(function(e){

        $('#confirm').attr('url', $(this).attr('url')).attr('target_id', $(this).attr('target_id'));

           confirm_comment($(this).attr('msg'));

        return false;

    });
    
    if ($("#menubar").length){
		$("#menubar ul li").hover(function(e){
			var obj = $(this);
			obj.children('a').animate({width: 'show'}, 300);
		},  function () {
			var obj = $(this);
			if (!obj.hasClass('selected')){
				obj.children('a').animate({width: 'hide'}, 300);
			}
		}
		);
	}

	//calendario da jquery
	if ($(".datepicker").length > 0){

        $(".datepicker").datepicker({
            changeMonth: true,
            changeYear: true,
			dateFormat: "dd/mm/yy"
        });

		$("div#ui-datepicker-div").css('z-index', '1000');

    }

    $('.commentIcon').click(
           function(e){

            var url = this.getAttribute('target');
               var id  = this.getAttribute('id');

            $.post(url, { id: id },
                  function(data){

                     if(!data.alert){

                        if (data.status == false){
                            $('#total_active').html( parseInt($('#total_active').html()) - 1);
                            $('#total_desactive').html( parseInt($('#total_desactive').html()) + 1);
                            $("#"+id).attr('title', 'Despublicado');
                            $("#"+id).html('<img src="/megavideo/static/manager/images/bt_despublicar.gif" /> Despublicado ');
                            $(".line_"+id).fadeOut();
                        }else{
                            $('#total_active').html( parseInt($('#total_active').html()) + 1);
                            $('#total_desactive').html( parseInt($('#total_desactive').html()) - 1);
                            $("#"+id).attr('title', 'Publicado');
                            $("#"+id).html('<img src="/megavideo/static/manager/images/bt_publicar.gif"/> Publicado ');
                            $(".line_"+id).fadeOut();
                        }

                    }else{

                        alert(data.alert);

                    }

                  },'json');

           }
    );

    $('.commentBtn').click(
            function(e){

                var url = this.getAttribute('target');
                var id  = this.getAttribute('id');

                $.post(url, { id: id },
                        function(data){

                    if(!data.alert){

                        if (data.status == false){
                            $('#span_total_active').html( parseInt($('#span_total_active').html()) - 1);
                            $('#span_total_desactive').html( parseInt($('#span_total_desactive').html()) + 1);
                            $("#"+id).attr('title', 'Despublicado').html('<img src="/megavideo/static/manager/images/bt_despublic.png" />');
                        }else{
                            $('#span_total_active').html( parseInt($('#span_total_active').html()) + 1);
                            $('#span_total_desactive').html( parseInt($('#span_total_desactive').html()) - 1);
                            $("#"+id).attr('title', 'Publicado').html('<img src="/megavideo/static/manager/images/bt_publicado.png"/>');
                        }

                    }else{

                        alert(data.alert);

                    }

                },'json');

            }
    );
    
    $('.publicado ').click(function(){
		pub_id = $(this).attr('id')
		id = pub_id.split('_')[1]
		target = $(this).attr('target')
		bk = $(this).css('background-position');
		animate = $(this) 
		
		$.post(target, {'id': id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()} , function(data){
			if(data.status){
				animate.stop().animate(
		 				{backgroundPosition:"(0px 0px)"}, 
		 				{duration:500});
			}else{
				animate.stop().animate(
		 				{backgroundPosition:"(-41px 0px)"}, 
		 				{duration:500});
			}
		})
	});
    

    $('.change_status').click(function(e){

        var url       = $(this).attr('url');
        var categoria = $(this).attr('categoria');
        var id        = $(this).attr('target_id');

         $.post(url, { value: id  },
             function(data){

                 if (data.published){

                    $("#total_desactive").html(parseInt($("#total_desactive").html()) - 1);
                    $("#total_active").html(parseInt($("#total_active").html()) + 1);

                    $('img.change_status').attr('src','/megavideo/static/manager/images/bt_published.gif').attr('title', 'Publicado');
					$('a.change_status').attr('title', 'Publicado').html("Publicado");

                 } else {

                    $("#total_desactive").html(parseInt($("#total_desactive").html()) + 1);
                    $("#total_active").html(parseInt($("#total_active").html()) - 1);

                    $('img.change_status').attr('src','/megavideo/static/manager/images/bt_despublished.gif').attr('title', 'Despublicado');
					$('a.change_status').attr('title', 'Despublicado').html("Despublicado");

                 }

        },'json');

    });

    $('.orderIcon').click(
           function(e){
            var url = this.getAttribute('target');
               var id  = this.getAttribute('id');

            $.post(url, { id: id },
                  function(data){
                    if (data.status == false){
                        $("#"+id).attr('title', 'Despublicado');
                    }else{
                        $("#"+id).attr('title', 'Publicado');
                    }
                  },'json');

           }
    );

    $('#bt_select_all').click(
           function(e){

               if($(this).attr('title') == 'checkall'){
                   $(this).attr('title','nocheckall');
                   $("input[type='checkbox']").attr('checked', false);
               }else{
                   $(this).attr('title','checkall');
                   $("input[type='checkbox']").attr('checked', true);
               }

         }
    );

   $('#btn_salvar_program').click(
     function(e){

        var url   = channel + "manager/program/ajaxupdateprogram/";
        var value = new Array();
        var index = new Array();

        $(".metaInput").each(function(e){
            index.push( $(this).attr('name') );
            value.push( $(this).val() );
        });

        $('#output_message').html("<img src='/megavideo/static/portal/images/loading.gif' border='0' />");

        $.post(url, { index: index, value: value, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
              function(data){
                if (data.status == false){
                    $('#output_message').css('background-color','#FF9A9A');
                    $('#output_message').css('color','#000');
                }else{
                    $('#output_message').css('background-color','#E1E3E7');
                    $('#output_message').css('color','#989CA9');
                }

                $('#output_message').empty();
                $('#output_message').hide()

                for (i in data.form_msg){
                    $('#output_message').append('<p> * ' + data.form_msg[i].msg + '</p>');
                    $('#output_message').slideDown();
                }
         },'json');

    });

    change_tabs('informacoes', 'menu_header_1');

    $('#content_menu ul li#informacoes').show();
    $('#menu_header ul li#menu_header_1').addClass('selected');

    $('.change_tabs').click(function(e){
        show_tab = $(this).attr('title');
        id_selected = $(this).attr('id');
        change_tabs(show_tab, id_selected );
    });

    $('.auto_save_category').click(function(e){

         var url          = channel + "manager/program/ajaxtogglecategory/";
         var video_id      = $('#hidden_video_id').val();
         var category_id   = $(this).val();

         $.post(url, { video_id: video_id , category_id: category_id }, function(data){} , 'json');

    });

    $("ul#slideToggleCategory ul").hide();

    $('.subcategory_toogle').click(
        function(e){

            var target = $(this).attr('id');
            icon = $(this).html();

            if (icon == '&nbsp;-&nbsp;'){
                $(this).html('+&nbsp;');
            }else{
                $(this).html('&nbsp;-&nbsp;');
            }

            $('ul .'+target).slideToggle("slow");
        }
    );

    if ($('#confirm').length > 0) {
        $('#confirm').jqm({
            overlay: 80,
            trigger: false
        });
    }

    if ($('#confirm').length > 0) {
        $('#confirm_categoria').jqm({
            overlay: 50,
            modal: false,
            trigger: false
        });
    }

    //monta menu
    montaMenu();
    
    //montar channel
    montaChannel();

	//invoca player
	if ($("div#flashPlayer").length > 0) {
		refreshPlayer($("div#flashPlayer").attr("name"));
	}

	//invoca o grafico da pagina
	if ($("div#graph_sumario").length > 0) {
		var so2 = new SWFObject("/megavideo/static/swf/vflowstat/OFC.swf", "graph_sumario_player", "100%", "312", "9.0.0");
		so2.addParam("wmode", "transparent");
		so2.addVariable("data-file", "/stat/graphsumarioid/" + $("div#graph_sumario").attr("name") + "/?pick=" + $("div#graph_sumario").attr("pick"));
		so2.addVariable("loading", "Carregando os dados gerais");
		so2.write("graph_sumario");
	}

	//function resizable para ampliar div
	if ($(".resizable").length > 0) {
		$(".resizable").resizable({
			grid: 50,
			ghost: true,
			animate: true,
			maxHeight: 500,
			maxWidth: 470,
			minHeight: 20,
			minWidth: 470
		
		});
	}

	$(".embed").click(function(e){

		var valor = $(this).attr('title');
		var arr = new Array();
		arr = valor.split('x');

		var video_id = $("#form_embed").attr('target');

		$(".embed").each(function(e){
			$(this).attr('class', 'embed');
		});

		$(this).attr('class', 'embed selected');

		$('#id_embed').attr('disabled', 'disabled');

		$.ajax({
			type: "POST",
			url: channel + "portal/optionembed/",
			dataType: "script",
			data: {width: arr[0], height: arr[1], video_id: video_id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()},
			success: function(e){
				$('#id_embed').val(e);
				$('#id_embed').attr('disabled', '');
			}
		});

	});
	
	
	try {
        $("body select.ddselect").msDropDown();
        $(".ddTitle span.arrow").before('<span class="before"><img src="/megavideo/static/manager/images/combo1.png" border="0" /></span>');
		$(".ddTitle span.arrow").after('<span class="after"><img src="/megavideo/static/manager/images/combo3.png" border="0" /></span>');
    } catch(e) {
        //alert("Error msDropDown: " + e);
    }
    
    try {
	    $(".ddselect_portal").css("z-index", "10000").msDropDown({visibleRows:15, rowHeight:23});
		$("#form .ddTitle span.arrow").before('<span class="before"><img src="/megavideo/static/manager/images/combo_portal_01.png" border="0" /></span>');
		$("#form .ddTitle span.arrow").after('<span class="after"><img src="/megavideo/static/manager/images/combo_portal_03.png" border="0" /></span>');
    } catch(e) {
        //alert("Error msDropDown: " + e);
    }

}

function publishVideo(bool, video_id){
	
	var url = '/manager/program/ajaxpublish/';
	$.post(url, { video_id : video_id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
		function(data){
			if (data.error != "0"){
				alert("Não foi possivel publicar esse video!");
			}
		}, 
	'json');

}

function addChannelType(channel_id, base_url){
	var url = base_url + 'add_channeltype/' + channel_id + '/';
	window.open( url ,
	'addUrl',
	'toolbar=0,status=0,width=626,height=436');
	return false;
}

function montaMenu(){

    $("img.bt_deletar").click(function(e){

        var url         = channel + "manager/program/category/ajaxdel/";
        var video_id    = $('div#blockCategory').attr("name");
        var category_id = $(this).attr("name");

        $.post(url, { video_id: video_id , category_id: category_id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
            function(data){
                if (data.status == true) {

                    $(".change_status").attr("categoria", data.count);

                    $('div#blockCategory').load(channel + 'manager/program/category/ajaxlistcategory/', {
                        'video_id': video_id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
                    }, function(e){
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
        $("input.category" + $(this).attr("name")).mcDropdown("#categorymenu" + $(this).attr("name"), {delim: " : ", allowParentSelect : false , select:function() { returnValue1() }});
    });

}

function montaChannel(){
	 $("img.bt_deletar_channel").click(function(e){

	        var url         = channel + "manager/program/channel/ajaxdel/";
	        var video_id    = $('div#blockChannel').attr("name");
	        var channel_id = $(this).attr("name");

	        $.post(url, { video_id: video_id , channel_id: channel_id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
	            function(data){
	                if (data.status == true) {

	                    $(".change_status").attr("categoria", data.count);

	                    $('div#blockchannel').load(channel + 'manager/program/channel/ajaxlistchannel/', {
	                        'video_id': video_id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
	                    }, function(e){
	                    	montaChannel();
	                    });

	                } else {

	                    alert("erro em deletar uma categoria!");

	                }
	            }, 'json');

	    });

    
   
    /* invoca combo */
    $("input.channel").each(function(e){
        $(this).attr("class", "channel" + $(this).attr("name"));
        $("input.channel" + $(this).attr("name")).mcDropdown("#channelmenu" + $(this).attr("name"), {delim: " : ", allowParentSelect : false, select:function() { returnValue2() } , className: 'itensChannel' });
    });

}

function refreshPlayer(video_id) {

    var so = new SWFObject("/megavideo/static/manager/swf/visualizador.swf", "flashPlayer_player", "452", "335", "9.0.0", "#000000");
    so.addVariable("base_url"       , $("div#flashPlayer").attr("url"));
    so.addVariable("idContent"      , $("div#flashPlayer").attr("name"));
    so.write("flashPlayer");

}

function cropthumb(time){
	
	var video_id = $("#flashPlayer").attr("name");
	
	url = "/megavideo/manager/set_thumb/" + video_id + "/";
	
	$.getJSON(url, { tempo: time }, function(data){
		//alert(data.error);
		if (data.error == "0"){
			refreshPlayer(video_id);
		}
	});
	
}

/* importante para a plugin jquery */
function returnValue1() {

    var itensCategory = new Array();
    var url           = channel + "manager/program/category/ajaxadd/";
    var video_id      = $('div#blockCategory').attr("name");
    
    
    
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

    $.post(url, { video_id: video_id, listcategory: itensCategory, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
        function(data){
            if (data.status == "True") {

                $(".change_status").attr("categoria", data.count);

                $('div#blockCategory').load(channel + 'manager/program/category/ajaxlistcategory/', {
                    'video_id': video_id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
                }, function(e){
                    montaMenu();
                });

            } else {

                alert("erro em deletar uma categoria!");

            }
        }, 'json');
    
    
    if ($('.sendbug').length){
		var options = { 
	        target:        '#bug_return',   // target element(s) to be updated with server response 
	        //success:       showResponse, // post-submit callback 
	        dataType:  'json',           // 'xml', 'script', or 'json' (expected server response type)
	        clearForm: true 
	    }; 
	    // bind form using 'ajaxForm' 
	    $('.sendbug').ajaxForm(options); 
	}

}

/* importante para a plugin jquery */
function returnValue2() {
	
    var itensChannel  = new Array();
    var url           = channel + "manager/program/channel/ajaxadd/";
    var video_id      = $('div#blockChannel').attr("name");
    
    $("input.itensChannel").each(function(e){
        var verifica = true;
        var valor    = $(this).val();
        
        for (var u in itensChannel){
            if (itensChannel[u] == valor){
                verifica = false;
            }
        }

        if (valor != "0" && valor != "" && verifica == true){
        	itensChannel.push($(this).val());
        }
    });
    
    $.post(url, { video_id: video_id, listchannel: itensChannel, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
        function(data){
            if (data.status == "True") {
                $(".change_status").attr("channel", data.count);
                
                $('div#blockChannel').load(channel + 'manager/program/channel/ajaxlistchannel/', {
                    'video_id': video_id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
                }, function(e){
                	montaChannel();
                });
            } else {
                alert("erro em deletar uma categoria!");
            }
        }, 'json');

}


function ajax_add_channel(obj) {
	
    var itensChannel  = new Array();
    var url           = channel + "manager/program/channel/ajaxadd/";
    var video_id      = $('div#blockChannel').attr("name");
    
    $(obj).attr('disabled', true);
    $('.concluido_channel').css('display', 'none');
    
    $.post(url, { video_id: video_id, listchannel: Array($(obj).val()), csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
    function(data){
        if (data.status == "True") {
        	$(obj).attr('disabled', false);
        	$('.concluido_channel').css('display', 'inline');
        } else {
            alert("erro em deletar uma canal!");
        }
    }, 'json');

}

function ajax_add_category(obj) {
	
    var itensChannel  = new Array();
    var url           = channel + "manager/program/category/ajaxadd/";
    var video_id      = $('div#blockChannel').attr("name");
    
    $(obj).attr('disabled', true);
    $('.concluido_category').css('display', 'none');
    
    $.post(url, { video_id: video_id, listcategory: Array($(obj).val()), csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
    function(data){
        if (data.status == "True") {
        	$(obj).attr('disabled', false);
        	$('.concluido_category').css('display', 'inline');
        } else {
            alert("erro em deletar uma canal!");
        }
    }, 'json');

}


function change_tabs(show_tab, id_selected){

    var tabs = new Array('informacoes', 'partes', 'comentarios', 'incorporar');

    $('#menu_header table tr td.change_tabs').removeClass('selected');

    for (i in tabs){
        if (tabs[i] == show_tab) {
            //$('#content_menu ul li#'+tabs[i]).fadeIn();
            $('table.content_menu tr#'+tabs[i]).css("z-index", 0).css("display", "block").css("border-top", "0px");
            $('#menu_header table tr td#'+id_selected).addClass('selected');
        } else {
            //$('#content_menu ul li#'+tabs[i]).hide();
            $('table.content_menu tr#'+tabs[i]).css("display", "none");
        }

    }

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

function strtofloat(str){

    if (str.indexOf(",")!= -1) {
        str = str.replace(",",".");
    }
    var result = parseFloat(str);
        if (isNaN(result)) {
        result = 0.0;
    }
    return result;

}

function confirm(msg, callback) {

    $('#confirm').jqmShow().find('p.jqmConfirmMsg').html(msg).end();
    $('table td.sim:visible, table td.no:visible').unbind('click');
    $('table td.sim:visible, table td.no:visible').bind('click', function(e){

        if(this.id == "1"){

            var id  = $('#confirm').attr('target_id');
            var url = $('#confirm').attr('url');

            $.post(url + 'del/', { id: id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
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

function confirm_comment(msg, callback) {

    $('#confirm').jqmShow().find('p.jqmConfirmMsg').html(msg).end();
    $('table td.sim:visible, table td.no:visible').unbind('click');
    $('table td.sim:visible, table td.no:visible').bind('click', function(e){

        if(this.id == "1"){

            var id  = $('#confirm').attr('target_id');
            var url = $('#confirm').attr('url');

            $.post(url, { id: id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
              function(data){
                if ( data.status == true ){

                    $('li.line_' + id).fadeOut();

                    $('span#span_total_active').html(data.total_active);
                    $('span#span_total_desactive').html(data.total_desactive);

                } else {
                    alert('Error ao excluir a informação');
                }
              }, 'json');

        }

        $('#confirm').jqmHide();

    });

}

function confirm_categoria(msg, callback) {

    $('#confirm_categoria').jqmShow().find('p.jqmConfirmMsg').html(msg).end();
    $('#confirm_categoria :button:visible').unbind('click');
    $('#confirm_categoria :button:visible').bind('click', function(e){

        $('#confirm_categoria').jqmHide();

    });

}

$(document).ready(init);
