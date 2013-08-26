(function($) {

	function set_tipo(tipo)
	{
		if (tipo == 0)
		{
			$('div.is_desc_g').css('display', 'block');
			if ( $('input[name=is_desc_g]').is(":checked") )
			{
				$("div.desc_g, div.is_image").css('display', 'block');
			} else {
				$("div.desc_g, div.is_image").css('display', 'none');
			}
			$('div.is_email, div.email, div.is_text, div.text').css('display', 'none');
		} else {
			$('div.is_email, div.is_text').css('display', 'block');
			if ( $('input[name=is_email]').is(":checked") )
			{
				$("div.email").css('display', 'block');
			} else {
				$("div.email").css('display', 'none');
			}
			$('div.is_desc_g, div.desc_g, div.is_image').css('display', 'none');
		}
	}

	$(document).ready(function($) {

		var obj = $('select[name=tipo]');
		set_tipo(obj.val());
		obj.change(function(e){
			set_tipo($(this).val());
		});

		var obj = $('input[name=is_desc_g]');
		obj.change(function(e){
			$("div.desc_g, div.is_image").slideToggle();
		});
		if ( ! $('input[name=is_desc_g]').is(":checked") ) {
			$("div.desc_g, div.is_image").css('display', 'none');
		}

		var obj = $('input[name=is_text]');
		obj.change(function(e){
			$("div.text").slideToggle();
		});
		if ( ! $('input[name=is_text]').is(":checked") ) {
			$("div.text").css('display', 'none');
		}

		var obj = $('input[name=is_email]');
		obj.change(function(e){
			$("div.email").slideToggle();
		});
		if ( ! $('input[name=is_email]').is(":checked") ) {
			$("div.email").css('display', 'none');
		}

	});

})(django.jQuery);