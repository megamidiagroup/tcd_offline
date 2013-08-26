(function($) {
	
	$(document).ready(function($) {
		var obj = $('#id_tipo');
		set_option(obj);
		obj.change(function(e){
			set_option($(this));
		});
		if ( $('#id_tipo_t').length )
		{
			var obj = $('#id_tipo_t');
			set_option(obj);
			obj.change(function(e){
				set_option($(this));
			});
		}
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
			
			switch(obj.val())
			{
				case 'M':
				case 'B':
				case 'K':
				  	$('#id_code, #id_destaq, .help').parent().parent().css('display', 'block');
					$('#id_agendado_0').parent().parent().parent().css('display', 'none');
					$('#id_agendado_0, #id_agendado_1').val('');
					break;
				/* para tipo de treinamento */
				case '0':
					$('#id_destaq, #id_tipo, #id_code, #id_time, #id_author, #id_desc_l').parent().parent().css('display', 'block');
					$('#id_treinamento, #id_idproduto, #id_preco, #id_datavalida').parent().parent().css('display', 'none');
					if ( $(".form-row div p input#id_file").length ){
						$('#id_file').parent().parent().parent().css('display', 'none');
					} else {
						$('#id_file').parent().parent().css('display', 'none');
					}
					if ( $(".form-row div p input#id_image1").length ){
						$('#id_image1').parent().parent().parent().css('display', 'none');
					} else {
						$('#id_image1').parent().parent().css('display', 'none');
					}
					if ( $(".form-row div p input#id_image2").length ){
						$('#id_image2').parent().parent().parent().css('display', 'none');
					} else {
						$('#id_image2').parent().parent().css('display', 'none');
					}
					if ( $(".form-row div p input#id_image3").length ){
						$('#id_image3').parent().parent().parent().css('display', 'none');
					} else {
						$('#id_image3').parent().parent().css('display', 'none');
					}
					if ( $(".form-row div p input#id_image4").length ){
						$('#id_image4').parent().parent().parent().css('display', 'none');
					} else {
						$('#id_image4').parent().parent().css('display', 'none');
					}
					$('div.image div label').html('Imagem do Vídeo');
					$('.form-row.required').css('display', 'block');
					break;
				case '1':
					$('#id_destaq, #id_tipo, #id_code, #id_time, #id_author, #id_desc_l, #id_idproduto, #id_preco, #id_datavalida').parent().parent().css('display', 'none');
					$('#id_treinamento').parent().parent().css('display', 'block');
					if ( $(".form-row div p input#id_file").length ){
						$('#id_file').parent().parent().parent().css('display', 'block');
					} else {
						$('#id_file').parent().parent().css('display', 'block');
					}
					if ( $(".form-row div p input#id_image1").length ){
						$('#id_image1').parent().parent().parent().css('display', 'none');
					} else {
						$('#id_image1').parent().parent().css('display', 'none');
					}
					if ( $(".form-row div p input#id_image2").length ){
						$('#id_image2').parent().parent().parent().css('display', 'none');
					} else {
						$('#id_image2').parent().parent().css('display', 'none');
					}
					if ( $(".form-row div p input#id_image3").length ){
						$('#id_image3').parent().parent().parent().css('display', 'none');
					} else {
						$('#id_image3').parent().parent().css('display', 'none');
					}
					if ( $(".form-row div p input#id_image4").length ){
						$('#id_image4').parent().parent().parent().css('display', 'none');
					} else {
						$('#id_image4').parent().parent().css('display', 'none');
					}
					$('div.image div label').html('Imagem da Página');
					$('.form-row.required').css('display', 'block');
					break;
				case '2':
				  	$('#id_destaq, #id_tipo, #id_code, #id_time, #id_author, #id_treinamento').parent().parent().css('display', 'none');
				  	if ( $(".form-row div p input#id_file").length ){
						$('#id_file').parent().parent().parent().css('display', 'none');
					} else {
						$('#id_file').parent().parent().css('display', 'none');
					}
					$('#id_idproduto, #id_preco, #id_datavalida, #id_desc_l').parent().parent().css('display', 'block');
					if ( $(".form-row div p input#id_image1").length ){
						$('#id_image1').parent().parent().parent().css('display', 'block');
					} else {
						$('#id_image1').parent().parent().css('display', 'block');
					}
					if ( $(".form-row div p input#id_image2").length ){
						$('#id_image2').parent().parent().parent().css('display', 'block');
					} else {
						$('#id_image2').parent().parent().css('display', 'block');
					}
					if ( $(".form-row div p input#id_image3").length ){
						$('#id_image3').parent().parent().parent().css('display', 'block');
					} else {
						$('#id_image3').parent().parent().css('display', 'block');
					}
					if ( $(".form-row div p input#id_image4").length ){
						$('#id_image4').parent().parent().parent().css('display', 'block');
					} else {
						$('#id_image4').parent().parent().css('display', 'block');
					}
					$('div.image div label').html('Imagem da Vitrine');
					$('.form-row.required').css('display', 'none');
				  	break;
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