$(document).ready(function(){

	try {
		$("#select").css("z-index", "10000").msDropDown({visibleRows:15, rowHeight:23});
		$(".ddTitle span.arrow").before('<span class="before"><img src="{{STATIC_URL}}/static/portal/images/left_bg.png" border="0" /></span>');
		$(".ddTitle span.textTitle").after('<span class="after"><img src="{{STATIC_URL}}/static/portal/images/right_bg.png" border="0" /></span>');
	} catch(e) {
		alert("Error msDropDown: " + e);
	} 

});

function selectcategory(url, obj){
	
	window.location = url + $(obj).val() + '/';
	
}

function selectchannel(obj){
	
	window.location = $(obj).val();
	
}