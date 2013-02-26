$(function () {
		$('#information').remove();
		$('#footer').remove();
		$('#logo_home a').attr('href', 'http://www.institutoiob.com.br')
		$('#main_logo').attr('src', '../portal/images/channels/logo_iob.png');
		$('#main_logo').attr('alt', 'IOB');
			if ($('#float_flash').length) 
		{ 	
		  $('.jquery-corner', $('#float_flash')).remove()
		}	
		})
