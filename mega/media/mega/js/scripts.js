var initial = false;

$(function() {
	
	// para proteger ie6
	if ($.browser.msie == true && $.browser.version <= 6){
		var url = $(".no-ie6").attr("url");
		$(".no-ie6").load(url + "noie6/");
	}
	
	var viewportWidth = $(window).width();
	
	$(".menu-button").click(function(){
		$("#header #menu ul").slideToggle("slow");
	});
	
	$(".search-button").click(function(){
		$("#search").slideToggle();
	});
	
	$("#menu .user-button").click(function(){
		$("#account").slideToggle();
		$("#enquete").slideUp();
	});
	
	$("#menu .enquete").click(function(){
		$("#enquete").slideToggle();
		$("#account").slideUp();
	});
	
	$(".certified h5 a").click(function(e){
		e.preventDefault();
		$(this).parent().parent().find(".courses").slideToggle();
	});
	
	$("#account-widget .user-account").click(function(e){
		e.preventDefault();
		e.stopPropagation();
		$("#account").toggle();
		$('#enquete').hide();
	});
	
	$("#enquete-widget .enquete").click(function(e){
		e.preventDefault();
		e.stopPropagation();
		$("#enquete").toggle();
		$('#account').hide();
	});
	
	$(document).click(function(event)
	{
		if(!$('#account-widget .user-account').is(':visible')){return;};
		if($('#account').is(':visible') && $(event.target).parents("#account").length == 0)
		{
			$('#account').hide();
		}
		if(!$('#enquete-widget .enquete').is(':visible')){return;};
		if($('#enquete').is(':visible') && $(event.target).parents("#enquete").length == 0)
		{
			$('#enquete').hide();
		}
	}); 
	
	$('#enquete-widget #enquete input[type=radio]').click(function(e){
		$('.btn').css('display', 'block');
	});      

	$(window).resize(function() {
		var w = $(window).width();
	  	if(w > 600)
		{
			$("#header #menu ul").show();
			$("#search").show();
		}
		
		if(viewportWidth != w)
		{
			viewportWidth = w;
			if($(".player").length)updatePlayer($(".player").width(), $(".player").height());
		}
		
		$('#content').css('height', 'auto');
		
		ajustaRodape();
	});
	
	function ajustaRodape()
	{
		var bodyHeight = $('body').outerHeight();
		var espaco = $(window).height() - bodyHeight;
		if(espaco > 0)
		{
			var newHeight = $('#content').height() + espaco;
			$('#content').css('min-height', newHeight);
		}
	}
	
	var count_total = 0;
    var count_load  = 0;
         
    $('#content img').each(function(e){
    	count_total++;
        $(this).css({'display' : 'none'});
    });
   
	$("#content img").one('load', function() {
         count_load++;
         $(this).fadeIn(1000);
         if (count_total == count_load){setTimeout(ajustaRodape, 10);}
    }).each(function() {
         if(this.complete) $(this).load();
    }) 
    
    if (count_total == 0){setTimeout(ajustaRodape, 10);}

    $('.flexslider').flexslider();
	
	var buttom = $('.btn_logout');
	
	buttom.attr('onclick', 'if (confirm("Deseja sair do sistema?")){window.location="' + buttom.attr('href') + '";}');
	buttom.attr('href', 'javascript:void(0);');
	
	if($(".player").length)updatePlayer($(".player").width(), $(".player").height());
	
});

function open_anexo(obj)
{
	var div_description = $(obj).parent().parent().find('div').eq(0);
	var div_anexo       = $(obj).parent().parent().find('.anexo');

	if ( div_anexo.attr('value') == 'false' )
	{
		div_anexo.find('.icon .open').delay(1000).fadeIn();
		div_description.slideUp("slow");
		div_anexo.find('ul').delay(400).slideDown("slow");
		div_anexo.find('.icon .close').fadeOut();
		div_anexo.attr('value', 'true');
	} else {
		div_anexo.find('.icon .close').delay(1000).fadeIn();
		div_description.delay(400).slideDown("slow");
		div_anexo.find('ul').slideUp("slow");
		div_anexo.find('.icon .open').fadeOut();
		div_anexo.attr('value', 'false');
	}
}

function open_faq(obj)
{
	var faq_video = $(obj).parent().parent();

	if ( faq_video.attr('value') == 'false' )
	{
		faq_video.find('fieldset ul.faq').slideDown("slow");
		faq_video.attr('value', 'true');
	} else {
		faq_video.find('fieldset ul.faq').slideUp("slow");
		faq_video.attr('value', 'false');
		_clear_send_faq();
	}
}

function open_send_faq(obj)
{
	var send_faq_video = $(obj).parent().parent().parent();

	if ( send_faq_video.attr('value') == 'false' )
	{
		send_faq_video.find('ul.send_faq').slideDown("slow");
		send_faq_video.find('ul.send_faq textarea').focus();
		send_faq_video.find('ul.faq').css('opacity', .5);
		$(obj).html("Cancelar");
		send_faq_video.attr('value', 'true');
	} else {
		_clear_send_faq();
	}
}

function open_send_faq_initial(obj)
{
	var send_faq_video = $(obj).parent();

	if ( send_faq_video.attr('value') == 'false' )
	{
		send_faq_video.find('ul.send_faq').slideDown("slow");
		send_faq_video.find('ul.send_faq textarea').focus();
		send_faq_video.find('ul.faq').css('opacity', .5);
		$(obj).html("Cancelar").css('opacity', .5);
		send_faq_video.attr('value', 'true');
	} else {
		_clear_send_faq();
	}
}

function send_faq(obj, url, token)
{
	
	var box = $(obj).parent().parent();

	if ( box.find('textarea').val().length == 0 )
	{
		box.find(".error").html('<span style="color: red">Digite a pergunta</span>');
		box.find('textarea').focus();
	} else {
		if ( box.find('textarea').val().length < 10 )
		{
			box.find(".error").html('<span style="color: red">A pergunta está muito curta, digite com mais números de caracteres.</span>');
			box.find('textarea').focus();
		} else {
			
			$(obj).val('Aguarde...').attr('disabled', true);
	    	
	    	$.ajax({
				url: url,
				type: 'POST',
				data: { csrfmiddlewaretoken : token, msg : box.find('textarea').val() },
				dataType: 'script',
				success: function(r) {
					
				}
			});
			
		}
	}
}

function clear_send_faq()
{
	setTimeout(_clear_send_faq, 3000);
}

function _clear_send_faq()
{

	var obj = $('.faq_video fieldset');
	
	if ( obj.attr('value') == 'true' )
	{
		obj.find('ul.send_faq').slideUp("slow");
		obj.find('ul.send_faq textarea').val('');
		obj.find('ul.faq').css('opacity', 1);
		if (initial){
			obj.find('legend').html("Faq do Treinamento - Enviar pergunta").css('opacity', 1);
		} else {
			obj.find('.faq li span').html("Enviar pergunta");
		}
		obj.attr('value', 'false');
		obj.find(".error").html('');
		obj.find("input[name=send_faq]").val('Enviar').attr('disabled', false);
	}
	
}

function set_mask(yes){}
