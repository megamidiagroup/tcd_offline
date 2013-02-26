var timeout = 500;
var closetimer = 0;
var ddmenuitem = 0;
//define e salva o ultimo texto para bloquear
var memory = '';

var blockanimation = false;

var ajax_timeout      = 700;
var ajax_closetimer   = null;

function init(){
	
	//Check browser version
	if($.browser.msie && $.browser.version=="6.0") {
		
		$('.pngfix').pngFix(); 
		
		//Function menu effects
		$('li.headlink').hover(
			function() {
				$('ol', this).css('display', 'block'); 
			},
			function() { 
				$('ol', this).css('display', 'none'); 
			}
		);
		
	}else{
		
		$('li.headlink').hover(
		//open
		function(e){
			jsddm_canceltimer();
			
			if (ddmenuitem != $('ol', this).attr('id')) jsddm_close();
			
			var position = $(this).position();
			ddmenuitem = $('ol', this).attr('id'); 
			$("#"+ddmenuitem).slideDown(300).css('z-index',9999).bgiframe();
			
		},
		//close
		function(e){
			jsddm_timer();
		});
		
	}
	
	$('.vote-star').rating({ 
		callback: function(value, link){ 
			var id_video = $('#id_video_hidden').val();
			
            $('input.vote-star').rating('disable');
			$('#captcha').html("<img src='/megavideo/static/portal/images/loading.gif' border='0' />");
			$('#captcha').load('/portal/ajaxcaptcha/', {'id_video': id_video , 'value': value }); 
		} 
	});
	
	
	//Create corner effect
	//if ($('#float_flash').length) $('#float_flash').corner('7px top cc:#161D25').corner('7px bottom cc:#dddfe1');
	//if ($('#float_list').length)  $('#float_list').corner('7px top cc:#0c1216').corner('7px bottom cc:#f2f2f2');
	
	//if ($('.corner-featured').length) $('.corner-featured').corner('5px top cc:#0b1116').corner('5px bottom cc:#edeeee');
	//if ($('.corner-listvideos-search').length) {
		//$('.corner-listvideos-search').corner('5px top cc:#0b1116').corner('5px bottom cc:#dddfe0');
	//} else {
		//if ($('.corner-listvideos').length) $('.corner-listvideos').corner('5px top cc:#c8cbcd').corner('5px bottom cc:#f0f0f0');
	//}
	
	
	$('#bt_pen').click( function(e){
 		$('#modal_form_tag').remove();
        id_video = $(this).attr('id_video');
 		$("#bt_show_videotag").append("<div id='modal_form_tag' style='display:none; position:absolute;'></div>");	
 		$('#modal_form_tag').load('/portal/ajaxtag/',{ id_video: id_video }, function(e){ 
			$('#modal_form_tag').show();	
		});
 	});
	
	$('.easytooltip').easyTooltip({ yOffset:-20, xOffset:-8 });
	
	$('#ajax_answer').hide();
	
	$('#ajax_search').focus(
			function(){
				var value = $(this).val();
				var filter = (value == 'Buscar') ? '' : value;
				$(this).val(filter);
			});
	
	$('#ajax_search').focusout(
			function(){
				var value = $(this).val();
				var filter = (value == '') ? 'Buscar' : value;
				$(this).val(filter);
			});

    $('#ajax_search').keyup(function(e){
        var $this = $(this);
        if ( $this.val().length > 2 ) {
	        $.ajax({
	            type     : "POST",
	            url      : '/portal/ajaxsearch/',
	            dataType : "html",
	            data     : {
	                'search' : $this.val(),
	                'channel' : $this.attr('chan'),
	                'cache'   : new Date().getTime()
	            },
	            success:
	                function(data){
	            		$("#ajax_answer").empty();
	            		$("#ajax_answer").html(data).fadeIn();
	                }
	        });
        }
    });

    $("#ajax_answer").mouseleave(function(e){
        timer_close_answer();
    }).mouseover(function(e){
        ajax_canceltimer();
    }).hide();
	
	if ($(".btn_incorporar").length){
		$(".btn_incorporar").click(function(e){
			var obj = $(this);
			obj.children('blockquote').delay(100).animate({width: 'show'}, 300);
			$(".btn_incorporar").each(function(e){
				var newobj = $(this);
				if ( obj.html() != newobj.html() ){
					newobj.children('blockquote').animate({width: 'hide'}, 300);
				}
			});
		});
	}
	
	if ($(".croptext").length) {
		$('.croptext').focus(function(e){
		
			var obj = $(this);
			var val = $(this).attr('val');
			
			if (obj.val() == val || obj.val() == '') {
				$(obj).val('');
			}
			
		}).blur(function(e){
		
			var obj = $(this);
			var val = $(this).attr('val');
			
			if (obj.val() == val || obj.val() == '') {
				$(obj).val(val);
			}
			
		});
		
	}
	
	$(".mouseover").mouseover(function(e){
		if ($(this).attr('open') == 'true') {
			$(this).stop().animate({
				opacity: .5
			}, 500);
		}
	}).mouseout(function(e){
		if ($(this).attr('open') == 'true') {
			$(this).stop().animate({
				opacity: 1
			}, 300);
		}
	}).mouseleave(function(e){
		if ($(this).attr('open') == 'true') {
			$(this).stop().animate({
				opacity: 1
			}, 200);
		}
	});
	
	$(".selectall").click(function(e){
		//alert($(this).val());
		$(this).focus(0);
		return false;
	});
	
}

function jsddm_close(){
    if (ddmenuitem) $("#"+ddmenuitem).slideUp();
}

function jsddm_timer(){
  	closetimer = window.setTimeout(jsddm_close, timeout);
}

function jsddm_canceltimer(){
    if (closetimer) {
        window.clearTimeout(closetimer);
        closetimer = null;
    }
}

function hideFormTagAjax(){
	
	$('#modal_form_tag').css('display' , 'none');
	
}

function timer_close_answer(){
	ajax_closetimer = window.setTimeout(ajax_close, ajax_timeout);
}

function ajax_canceltimer(){
	//console.log('ajax_canceltimer');
    if (ajax_closetimer) {
        window.clearTimeout(ajax_closetimer);
        ajax_closetimer = null;
    }
}

function ajax_close(){
	//console.log('ajax_close');
	$('#ajax_answer').fadeOut();
}

function sendCaptcha(target, output){
	var options = { 
	    type:    'post',         
	    target:  '#' + output	 
	}; 
	$('#' + target).ajaxSubmit(options);
    return false; 
}

//enviar commentario e return da resposta;
function setComment(target, id_target, video_id) {

	var nome    = $(target + " input#nome");
	var email   = $(target + " input#email");
	var msg     = $(target + " textarea#msg");
	
	var error   = $(target + " tr td.msg");
	
	var status  = $('td.bt_enviar img').attr('name');
	var action  = $(target).attr('action');
	var video_id = $(target).attr('video_id');
	
	
	if (status == "0"){
		return false;
	}
	
	if (nome.val() == "" || nome.val() == undefined){
		error.html('Digite seu nome!').css('color', '#DB0000');
		nome.focus();
		return false;
	}
	
	if (email.val() == "" || email.val() == undefined){
		error.html('Digite o e-mail!').css('color', '#DB0000');
		email.focus();
		return false;
		
	} else {
		
  		if ( (email.val().length < 6) || (email.val().indexOf("@") < 1) ){
			error.html('E-mail Inválido!').css('color', '#DB0000');
			email.focus();
			return false;
  		} else {
			var arr = new Array();
			arr = email.val().split('@');
			if (arr[0].length < 3 || arr[1].length < 4 || arr[1].indexOf('.') < 1){
				error.html('E-mail Inválido!').css('color', '#DB0000');
				email.focus();
				return false;
			}
		}
		
	}
	
	if (msg.val() == "" || msg.val() == undefined){
		error.html('Digite a mensagem!').css('color', '#DB0000');
		msg.focus();
		return false;
	} else {
		if (msg.val().length < 5){
			error.html('Digite uma mensagem com conteúdo! (maior que 5 letras)').css('color', '#DB0000');
			msg.focus();
			return false;
		}
	}
	
	$('td.bt_enviar img').attr('name', '0').css('opacity', '.4').css('cursor', 'default');
	error.html(' Aguarde, enviando ... ').css('color', '#DB0000');
	
	$.ajax({
		type: "POST",
		url: action,
		dataType: "json",
		data: {
			'video_id' : video_id,
			'nome'    : nome.val(),
			'email'   : email.val(),
			'msg'     : msg.val()
		},
		success: function(e){
			if (e.status){
				alert('AUT');
				$('.list_comments').empty();
				$(".more").attr('page', '1');
				error.html(' Enviado com sucesso! ').css('color', '#10AC0A');
				setTimeout("MorePage('.more', '" + video_id + "');$('.comment_list').slideUp(700);", 1000);
			} else {
				error.html(e.msg).css('color', '#DB0000');
			}
		}
	});
	
}

function load_comments(page, id_target, video_id){
	
	var action = '/portal/ajax_comment_list/';
	
	$.ajax({
		type: "POST",
		url: action,
		dataType: "html",
		data: { 'page' : page, 'video_id' : video_id },
		success: function(data){
			$('.list_comments').empty();
			$(id_target).html(data).slideDown(700);
		}
	});
	
}

function commentsform(obj, target){
	
	var video_id = $(obj).attr('video_id');
	var open    = $(obj).attr('open');
	
	if (open == '0'){
		$(obj).attr('open', '1').css('opacity', 0.5);
	} else {
		$(obj).attr('open', '0').css('opacity', 1);
	}
	
	$(target).slideToggle();
	
}

function MorePage(obj, video_id){
	
	var action = '/portal/ajax_comment_list/';
	var page   = $(obj).attr('page');

	$.ajax({
		type: "POST",
		url: action,
		dataType: "html",
		data: { 'page' : page, 'video_id' : video_id },
		success: function(data){
			$(".page" + page).html(data).slideDown(700);
			$(obj).attr('page', (parseInt(page) + 1));
		}
	});
	
}

function controlePress(valor){
	//define numero de caracteres para envio de comment
	var quant_limit = 200;
	var quant = (quant_limit - valor.value.length);
	$("table.comment tr td.caracter").html(quant);
	
	if (quant <= 0) {
		valor.value = memory;
		return false;
	} else {
		memory = valor.value;
		return true;
	}
}

function get_super_seta(idelement, obj, pos){
	
	var page = parseInt($(obj).attr("page"));
	var chan = $(obj).attr("chan");

	if ( page <= 0 || page > parseInt($(obj).attr("max")) ) return false;
	
	$("#" + idelement + " div.setaup").attr('page', (page - 1));
	$("#" + idelement + " div.setadown").attr('page', (page + 1));
	
	if ($("#" + idelement + " div.page_" + page).length){
		
		if (pos == 'up'){
			$("#" + idelement + " div.page_" + (page)).delay(100).slideDown('fast');
			$("#" + idelement + " div.page_" + (page + 1)).slideUp('fast');
		} else {
			$("#" + idelement + " div.page_" + (page - 1)).slideUp('fast');
			$("#" + idelement + " div.page_" + (page)).delay(100).slideDown('fast');
		}
		
		$("#" + idelement + " div.paginator").css('opacity', 1);
		
		return false;
	}
	
	$("#" + idelement + " div.paginator").css('opacity', .3);
	
	var action = chan + 'ajaxsuperlistvideos/' + page + '/';
	
	$.ajax({
		type: "POST",
		url: action,
		dataType: "html",
		data: {idelement : idelement},
		success: function(content){
			$("#" + idelement + " div.page_" + (page - 1)).slideUp('fast');
			$("#" + idelement + " div.page_" + (page - 1)).after('<div class="page_' + (page) + ' paginator">' + content + '</div>');
			$("#" + idelement + " div.page_" + (page)).css('display', 'none').delay(100).slideDown('fast');
			$("#" + idelement + " div.paginator").css('opacity', 1);
		}
	});
	
}

function open_form_comment($element, $buttom){
	
	$($element).slideToggle('show', function(e){
		if ($($buttom).attr('open') == 'true') {
			$($buttom).css("opacity", .4).attr('open', 'false');
		} else {
			$($buttom).css("opacity", 1).attr('open', 'true');
		}
	});
	
}

function all_comment(video_id, limit ) {
	
	var action = $(".list_comments").attr('action');
	var page   = $("a.more").attr('page');
	
	$.ajax({
		type: "POST",
		url: action,
		dataType: "html",
		data: {video_id : video_id, page : page, position : 'all', limit : 10},
		
		success: function(data){
			$(".list_comments").empty();
			$(".list_comments").html(data);
			$(".comments").css('opacity', 0).animate({opacity : 1}, 300);
			$(".more").attr("onclick", "").css("opacity", .2).css("cursor", "default");
		}
	});
	
}

function send_form($element){
	
	var arr = $($element).serializeArray();
	var video_id = 0;
	
	for (var i in arr){
		switch(arr[i].name) {
			case "nome":
			    if (arr[i].value == 'Nome' || arr[i].value == '') {
					$('.error i').html('Informe seu Nome!');
					$("input[name=" + arr[i].name + "]").focus();
					return false;
				} else {
					break;
				}
			case "email":
				if (arr[i].value == 'E-mail' || arr[i].value == '') {
					$('.error i').html('Informe seu E-mail!');
					$("input[name=" + arr[i].name + "]").focus();
					return false;
				} else {
					if (!verifica_email(arr[i].value)) {
						$('.error i').html('E-mail está incorreto!');
						$("input[name=" + arr[i].name + "]").focus();
						return false;
					} else {
						break;
					}
				}
			case "msg":
				if (arr[i].value == '' || arr[i].value.length < 10) {
					$('.error i').html('Faça seu comentário, no minimo 10 letras!');
					$("textarea[name=" + arr[i].name + "]").focus();
					return false;
				} else {
					break;
				}
			case "video_id":
				video_id = parseInt(arr[i].value);
				if (arr[i].value == '') {
					$('.error i').html('O vídeo não existe!');
					return false;
				} else {
					break;
				}
			default: 
				alert('houve algum erro grave!');
		}

	}
	
	$('.error i').html('Aguarde, enviando seu comentário ...');
	
	var serial = $($element).serialize();
	var action = $("#form").attr('action');
	
	$.ajax({
		type: "POST",
		url: action,
		dataType: "json",
		data: serial,
		success: function(e){
			if (e.status){
				$(".send_form").delay(3000).slideUp('show', function(e){
					closeComment();
				});
				
				var action = $(".list_comments").attr('action');
				var page   = $("a.more").attr('page');
				
				$.ajax({
					type: "POST",
					url: action,
					dataType: "html",
					data: {video_id : video_id, page : page, position : 'top'},
					success: function(data){
						$(".comments:first").before(data);
						$(".comments:first").css('opacity', 0).animate({opacity : 1}, 300);
					}
				});
				
				$('.error i').css('color', '#009c06').html('Comentário enviado com sucesso!');
				$(".countcomment").html( ( parseInt($(".countcomment").html()) + 1 ) );
			} else {
				$('.error i').html('Não foi possível enviar o seu comentário, contacte o administrador!');
			}
		}
	});
	
}

function set_list_coment(video_id, position, obj){

	var action = $('.list_comments').attr('action');
	var page   = $(obj).attr('page');
	
	$.ajax({
		type: "POST",
		url: action,
		dataType: "html",
		data: {video_id : video_id, page : page, position : position},
		success: function(data){
			$(".comments:last").after(data);
			$(".comments:last").css('opacity', 0).animate({opacity : 1}, 300);
			$(obj).attr('page', ( parseInt($(obj).attr('page')) + 1 ));
		}
	});
	
}

function closeComment(){
	
	$(".opencomment").css("opacity", 1).attr('open', 'true');
	$('.error i').html('').css('color', '#910004');
	
	var arr = $("#form").serializeArray();
	
	for (var i in arr){
		switch(arr[i].name) {
			case "nome":
			case "email":
				$("input[name=" + arr[i].name + "]").val($("input[name=" + arr[i].name + "]").attr('val'));
				break;
			case "msg":
				$("textarea[name=" + arr[i].name + "]").val($("textarea[name=" + arr[i].name + "]").attr('val'));
				break;
		}

	}
	
}

function verifica_email(str){

	var filter = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
	if (filter.test(str)) {
		return true;
	} else {
        return false;
    }
	
}

function set_size_flash(size, pos){
	if ( pos == 'true' ){
		$('div#featured').fadeOut();
		$('div#warp').css('margin-top', '120px');
	} else {
		$('div#featured').fadeIn();
		$('div#warp').css('margin-top', '0px');
	}
	$('object#flashPlayer').attr('width', size.split("x")[0]).attr('height', size.split("x")[1]);
	$('div#float_flash').css('width', size.split("x")[0] + 'px').css('height', size.split("x")[1] + 'px');
}

$(document).ready(init);
