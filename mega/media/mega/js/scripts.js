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
	
	if ($('.nops-user-button').length )$('.user-button').css('display', 'none');

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

	$("#menu .technical").click(function(){
		window.location = $('a.technical').attr('href');
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

	/*
	$("#technical-widget .technical").click(function(e){
		e.preventDefault();
		e.stopPropagation();
		$("#technical").toggle();
		$('#account, #enquete').hide();
	});
	*/

	$(document).click(function(event)
	{
		if ( $('#account-widget').length )
		{
			if(!$('#account-widget .user-account').is(':visible')){return;};
			if($('#account').is(':visible') && $(event.target).parents("#account").length == 0)
			{
				$('#account').hide();
			}
		}
		if ( $('#enquete-widget').length )
		{
			if(!$('#enquete-widget .enquete').is(':visible')){return;};
			if($('#enquete').is(':visible') && $(event.target).parents("#enquete").length == 0)
			{
				$('#enquete').hide();
			}
		}
		/*
		if ( $('#technical-widget').length )
		{
			if(!$('#technical-widget .technical').is(':visible')){return;};
			if($('#technical').is(':visible') && $(event.target).parents("#technical").length == 0)
			{
				$('#technical').hide();
			}
		}
		*/
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

	$('#content img').each(function(e){
    	var src        = $(this).attr('src');
    	var static_url = $('.static_url').attr('media');
    	$(this).attr('src', static_url + 'images/grey.gif');
    	$(this).attr('data-original', src);
	});

	$("#content img").lazyload({
		effect : "fadeIn",
		appear : function(elements_left, settings) {
			//console.log(this, elements_left, settings);
			ajustaRodape();
		}
	});

	setTimeout(ajustaRodape, 10);

	$('#content ul.videos li a.disabled, ' +
		'#content .related-videos li a.disabled, ' +
			'#account-widget #account .courses li a.disabled, ' +
				'#content ul.category li a.disabled'
	).each(function(e){
		$(this).css('opacity', .3).attr('href', 'javascript:void(0);').attr('onclick', '$(this).parent().find("p.msg_block").fadeIn().delay(3000).fadeOut(200)');
	});

    $('.flexslider').flexslider();

    if ( $("a.btn_overlay").length )
	{
		$("a.btn_overlay").css('opacity', .3);
	}

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

function send_ajax_etechnical($this, textarea, error, token)
{
	var text = $('textarea[name=' + textarea + ']');
	var btn  = $($this);

	$('span.' + error).css("color", "red");

	if ( btn.html() == 'Enviar' )
	{

		if ( text.val().length == 0 )
		{
			$('span.' + error).html('* Preencha o campo com sua mensagem.').fadeIn();
			text.focus();
		} else {
			if ( text.val().length < 8 )
			{
				$('span.' + error).html('* Sua mensagem está muito curta.').fadeIn();
				text.focus();
			} else {
				$('span.' + error).html('').fadeOut(100);
				btn.html('ENVIANDO...').css('opacity', .5);
				text.attr('disabled', true);

				$.ajax({
					url: btn.attr('action'),
					type: 'POST',
					data: { csrfmiddlewaretoken : token, msg : text.val() },
					dataType: 'script',
					success: function(r) {

					}
				});

			}
		}

	}

}

function set_mask(yes){}
