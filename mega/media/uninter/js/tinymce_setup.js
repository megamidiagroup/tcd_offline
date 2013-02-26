(function($) {
	$(document).ready(function(){
		
		$('textarea:first').each(function(e){
			$(this).addClass('mceEditor');
		});
		
		tinyMCE.init({
		        theme : "advanced",
		        mode : "specific_textareas",
		        editor_selector : "mceEditor",
		        language : "pt",
		        skin : "o2k7",
		        skin_variant : "silver",
		        width : "800",
		        height : "400",
				force_br_newlines : true,
		        force_p_newlines : false,
		        forced_root_block : '',

		        theme_advanced_fonts : 	"Arial=arial,helvetica,sans-serif;" +
								        "Arial Black=arial black,avant garde;" +
								        "Verdana=verdana,geneva;",
				
				theme_advanced_font_sizes : "10px,12px,14px,16px,24px",
				
				plugins : "fullscreen, table, preview",
		
				// Theme options
				theme_advanced_buttons1 : "newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,formatselect,fontselect,fontsizeselect,|,preview",
				theme_advanced_buttons2 : "cut,copy,paste,pasteword,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,code,|,forecolor,backcolor,fullscreen,|,tablecontrols",
		
				theme_advanced_toolbar_location : "top",
				theme_advanced_toolbar_align : "left",
				theme_advanced_statusbar_location : "bottom",
				theme_advanced_resizing : true
		});
		
	});
})(django.jQuery);

function getUrlVars() {
	
    var hashes = window.location.href.slice().split('/');
    var quant  = hashes.length;
    var id     = hashes[quant - 2];

    return id;
}