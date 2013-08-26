(function($) {
	
	$(document).ready(function($) {

		var obj = $('input[name=is_video]');
		obj.change(function(e){
			$("div.code").slideToggle();
			$("div.link").slideToggle();
		});
		if ( ! $('input[name=is_video]').is(":checked") ) {
			$("div.code").css('display', 'none');
		} else {
			$("div.link").css('display', 'none');
		}
		
		var obj = $('input[name=is_full_user]');
		obj.change(function(e){
			$("div.is_user_view").slideToggle();
		});
		if ( $('input[name=is_full_user]').is(":checked") ) {
			$("div.is_user_view").css('display', 'none');
		}
		
	});

})(django.jQuery);