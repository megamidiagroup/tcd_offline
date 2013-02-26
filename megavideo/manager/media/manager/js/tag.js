function init(){
	
	if ($("#playerFlash").length > 0) {

        var so = new SWFObject("/megavideo/static/manager/swf/tagueamento.swf", "playerTag", "430", "335", "9.0.0");
        so.addVariable("base_url"  , $("#playerFlash").attr("url"));
        so.addVariable("idContent" , $("#playerFlash").attr("video_id"));
        so.write("playerFlash");

	}
	
	if ($("#menubar").length){
		$("#menubar ul li").hover(function(e){
			var obj = $(this);
			obj.children('a').animate({width: 'show'}, 300);
		},  function () {
			var obj = $(this);
			if (!obj.hasClass('selected')){
				obj.children('a').animate({width: 'hide'}, 300);
			}
		}
		);
	}
	
	try {
        $("body select.ddselect").msDropDown();
        $(".ddTitle span.arrow").before('<span class="before"><img src="/megavideo/static/manager/images/combo1.png" border="0" /></span>');
		$(".ddTitle span.arrow").after('<span class="after"><img src="/megavideo/static/manager/images/combo3.png" border="0" /></span>');
    } catch(e) {
        //alert("Error msDropDown: " + e);
    }
}

function settag(idtag, timer, tag){
	
	var video_id = $("#playerFlash").attr("video_id");
	
	//alert("settag: " + idtag + " - timer: " + timer + " - tag: " + tag + " - video_id: " + video_id);

    if ( parseInt(idtag) > 0 ) {
        var url  = "/megavideo/manager/program/ajaxedittag/";
        var data = {id: idtag, tag: "\"" + tag + "\"", timer: timer, video_id: video_id};
    } else {
        var url  = "/megavideo/manager/program/ajaxaddtag/";
        var data = {id: video_id, tag: "\"" + tag + "\"", timer: timer};
    }

    $.ajax({
        type: "POST",
        url: url,
        dataType: "json",
        data: data,
        success: function(data){
            if ( data.status == true ){
                reflashTags(video_id);
            } else {
                if (data.duplic == true) {
					alert(data.duplic);
                } else {
					alert(data.status);
                }
            }
        }
    });
	
}

function reflashTags(video_id){

    $('#list_tag_float').load('/megavideo/manager/program/ajaxlisttags/', {'video_id': video_id});

}

function deletar_tag(idtag) {
	
	var url     = "/megavideo/manager/program/ajaxdeltag/";
	var video_id = $("#playerFlash").attr("video_id");

	$.ajax({
		type : "POST",
		url	: url,
		dataType : "json",
		data : {id_tag: idtag},
		success: function(data){
			if (data.status == true) {
				reflashTags(video_id);
			} else {
				alert("Erro ao salvar, tente novamente!");
			}
		}
	});

}

function editar_tag(idtag, tag, timer){

    var video_id = $("#playerFlash").attr("video_id");
	
	//alert("idtag: " + idtag + " - tag: " + tag + " - timer: " + timer + " - video_id: " + video_id);

	setPlayer(idtag, tag, timer);

}

function setPlayer(idtag, tag, timer) {

	var navegador;

	if(window.playerTag) navegador = window.document["playerTag"];
	if(document.playerTag) navegador = document.playerTag;

	navegador.pointsFlash(idtag, tag, timer);

}

$(document).ready(init);
