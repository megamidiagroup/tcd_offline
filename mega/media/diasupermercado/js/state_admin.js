(function($) {
	
	$(document).ready(function($) {

	    $("select[name='estado']").change(function(e){
	    	
	    	var select = $("select[name='cidade']");
	    	
	    	select.html('<option>Aguarde...</option>').attr('disabled', true);
	    	
	    	var obj = $(this);
	    	$.ajax({
				url: '/cities/' + obj.val() + '/',
				type: 'POST',
				data: {id : obj.val()},
				dataType: 'script',
				success: function(r) {
					var data = eval(r);
					var tmp  = '';
					for (var i=0; i < data.length; i++)
					{
						tmp += '<option value="' + data[i].id + '">' + data[i].name + '</option>';
					}
					select.html(tmp).attr('disabled', false);
				}
			});
			
	    });
	    
	});

})(django.jQuery);