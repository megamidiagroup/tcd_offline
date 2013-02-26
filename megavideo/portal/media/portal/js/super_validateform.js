/*
 * @autor Rafael Feijó da Rosa
 * @version 2.0
 * @decription: Para validar os campos item por item.
 * 
 */

(function($) {
	
	$.fn.superValidator = function(options) {
		$(this).click(function() { 
		
			var result = $.superValidator(options);
			
		});
	};
	
	$.superValidator = function(options) {
		
		// merge options with defaults
		var merged_options = $.extend({}, $.superValidator.defaults, options);
		
		var objetos = $('.sval').length;
		var cont    = 0;

		$('.sval').each(function(e){
			var validator = $.superValidator.validate($(this), merged_options);
			if ( validator.foc ) $(this).focus();
			if ( ! validator.error ) {
				$(merged_options.errorDiv).hide().html(validator.message).fadeIn();
			} else {
				cont++;
			}
			return validator.error;	
		});
		
		if (objetos === cont) {
			$(merged_options.errorDiv).hide().html('<span style="color:#00B70E;">Por favor, aguarde ...</span>').fadeIn();
			options.onSuccess();
		}

	};
	
	$.superValidator.validate = function(obj, opts) {

		var valAttr 		= obj.val();
		var css 			= opts.errorClass;
		var mail_filter 	= /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
		var numeric_filter 	= /(^-?\d\d*\.\d*$)|(^-?\d\d*$)|(^-?\.\d\d*$)|(^-?\d*$)/;
		var result 			= false;
		var errorTxt 		= 'default';
		
		// Validação de string sobre campo obrigatório
		if (obj.hasClass("sval")) {
			var rules = obj.attr("rules");
			var arr   = rules.split("|");
			var obrig = arr[0];
			var type  = arr[1];
			var limit = arr[2];
			var msg   = arr[3];
			var focus = arr[4];
			var foc   = false;
			
			if ( focus == 'focus' ) foc = true;

			if ( obrig == "*" ){
				if ( valAttr != "" ){
					
					/* validações */
					
					/* string */ 
					if ( type == 'string' ){
						if ( valAttr.length < limit.split(':')[0] ){
							return { error : result, message : msg + " (mínimo " + limit.split(':')[0] + " letras!)", foc : foc };
						}
						if ( valAttr.length >= limit.split(':')[1] ){
							return { error : result, message : msg + " (máximo " + limit.split(':')[1] + " letras!)", foc : foc };
						}
					}
					/* email */
					if ( type == 'email' ) if ( ! mail_filter.test(valAttr) ) return { error : result, message : msg + ' (está incorreto!)', foc : foc };
					/* numeric */
					if ( type == 'numeric' ) if ( ! numeric_filter.test(valAttr) ) return { error : result, message : msg, foc : foc };
					/* date */
					if ( type == 'date' ){
						var array = valAttr.split(opts.dateSeperator);
						var curDate = new Date();

						if (array.length < 3) {
							return { error : result, message : msg, foc : foc };
						} else {
							if ( ! (array[0] <= 12) && (array[1] <= 31) && (array[2] <= curDate.getFullYear()) ) return { error : result, message : msg, foc : foc };
						}

					}
					
				} else {
					return { error : result, message : msg, foc : foc };
				}
			}
		}
		
		return { error : true, message : '', foc : false };

	};
	
	// CUSTOMIZE HERE or overwrite by sending option parameter
	$.superValidator.defaults = {
		onSuccess		:	null,
		onError			:	null,
		scope			:	'',
		errorClass		:	'error-input',
		errorDiv		:	'#warn',
		errorMsg		: 	{
								reqString		:	'Erro ao validar a descrição',
								reqDate			:	'Erro ao validar a data!',
								reqNum			:	'Erro ao validar o número',
								reqMailNotValid	:	'Erro ao validar o e-mail!',
								reqMailEmpty	:	'O campo e-mail é requerido ',
								reqSame			:	'Os valores tem que ser iguais!',
								reqBoth			:	'Ambos são requeridos',
								reqMin			:	'O campo precisa conter pelo menos %1 caracteres'
							},
		customErrMsg	:	'',
		extraBoolMsg	:	'',
		dateSeperator	:	'.',
		extraBool		:	function() { return true; }
	};
})(jQuery);