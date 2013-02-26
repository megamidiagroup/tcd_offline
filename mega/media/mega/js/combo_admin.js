(function($) {
	
	$(document).ready(function($) {
		var obj = $('#id_tipo');
		set_option(obj);
		obj.change(function(e){
			set_option($(this));
		});
	});
	
	function set_option(obj)
	{
		
		if ( $("form#menu_form").length )
		{
			if (obj.val() == 'D'){
				CKEDITOR.replace("id_name", {"filebrowserWindowWidth": 800, "width": 700, "skin": "django", "filebrowserWindowHeight": 300, "filebrowserBrowseUrl": "/ckeditor/browse/", "filebrowserUploadUrl": "/ckeditor/upload/", "toolbar": "Full", "height": 100});
				$('#id_url, #id_order').parent().parent().css('display', 'none');
				$('#id_url').val(' ');
			} else {
				if (CKEDITOR.instances['id_name']) 
				{
					CKEDITOR.instances['id_name'].destroy();
				}
				$('#id_url, #id_order').parent().parent().css('display', 'block');
			}
			if (obj.val() == 'S'){
				$('#id_order').parent().parent().css('display', 'none');
				$('#id_url').val('busca/');	
			}
			$('#id_name').css('height', '16px').css('width', '220px');
		}
		
		if ( $("form#treinamento_form").length )
		{
			if (obj.val() == 'L'){
				$('#id_code, #id_destaq').parent().parent().css('display', 'none');
				$('#id_agendado_0').parent().parent().css('display', 'block');
				$('#id_code').val('');
			} else {
				$('#id_code, #id_destaq').parent().parent().css('display', 'block');
				$('#id_agendado_0').parent().parent().css('display', 'none');
				$('#id_agendado_0, #id_agendado_1').val('');
			}
		}
		
		if ( $("form#template_form").length )
		{
			if ( $('#id_tipo option[value=' + obj.val() + ']').html() == 'mega' ){
				$('.aligned, .cor6, .cor7, .cor37, .cor38').css('display', 'block');
			} else {
				$('.aligned, .cor6, .cor7, .cor37, .cor38').css('display', 'none');
				$('.name, .title_d, .custom').parent().css('display', 'block');
			}
		}
		
	}

})(django.jQuery);