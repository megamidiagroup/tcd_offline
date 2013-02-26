function init(){
	
	getActionsButtons();
	
	$(".new").css("display", "none");
	
    try {
        $('#confirm').jqm({overlay : 80, modal : true, trigger : false });
    } catch(e){}
	
	$("#filtro tr td").click(function(e){
		var filtro = $(this).attr("id");
		getList(0, filtro);
		$("#filtro tr td").each(function(e){
			$(this).removeClass();
		});
		$(this).addClass("selected");
	}).css("cursor", "pointer");
    
	
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
			$(".ddselect").css("z-index", "10000").msDropDown({visibleRows:15, rowHeight:23});
			$(".ddTitle span.arrow").before('<span class="before"><img src="/megavideo/static/manager/images/combo1.png" border="0" /></span>');
			$(".ddTitle span.arrow").after('<span class="after"><img src="/megavideo/static/manager/images/combo3.png" border="0" /></span>');
		} catch(e) {
			alert("Error msDropDown: " + e);
		} 
	
}

function newPublicity() {
	
	setPlayer(0);
	$(".new").css("display", "none");
	
}

function refleshList() {
	
	getList(0);
	getActionsButtons();
	
}

function getActionsButtons() {
	
	// do exclude with redirection
    $('.exclude').click(function(e){

        $('#confirm').attr('url', $(this).attr('url')).attr('target_id', $(this).attr('target_id'));

           confirm($(this).attr('msg'));

        return false;

    });
	
	setPlayer(0);
	
	$(".publicity_published").click(function(e){
		
		var obj = $(this);
		var id  = $(this).attr("id");
		var url = $("#playerFlash").attr("rota");
		$.post(url + 'ajaxpublished/', { id: id },
			function(data) {
				if ( data.status == true ){
					obj.attr("src", "/megavideo/static/manager/images/bt_publicado.png");
				} else {
					obj.attr("src", "/megavideo/static/manager/images/bt_despublic.png");
				}
			}, 
		'json');
		
	}).css("cursor", "pointer");
	
	$(".new").css("display", "none");
	
	$("table.list_publicity tr td.listagem table tr:odd").addClass("color");
	
}

function getList(idpublicity, filtro) {
	
	var url     = $("#playerFlash").attr("rota");
	var video_id = $("#playerFlash").attr("video_id");
	
	$(".listagem").load(url + 'ajaxlist/', { video_id: video_id, filtro: filtro }, 
		function(e){
			if (idpublicity == 0){
				getActionsButtons();
			}
		}
	);
	
	return false;
	
}

function setPlayer(idpublicity){

	if ($("#playerFlash").length > 0) {
	
		var so = new SWFObject("/megavideo/static/manager/swf/publicity.swf", "playerPublicity", "640", "360", "9.0.0");
		so.addVariable("base_url", $("#playerFlash").attr("url"));
		so.addVariable("idContent", $("#playerFlash").attr("video_id"));
		so.addVariable("idPublicity", idpublicity);
		//so.addVariable("versao", "true");
		so.write("playerFlash");
		
	}
	
}

function editar_publicity(idpublicity){
	setPlayer(idpublicity);
	$(".new").css("display", "block");
}

function confirm(msg, callback) {

    $('#confirm').jqmShow().find('p.jqmConfirmMsg').html(msg).end();
    $('table td.sim:visible, table td.no:visible').unbind('click');
    $('table td.sim:visible, table td.no:visible').bind('click', function(e){

        if(this.id == "1"){

            var id  = $('#confirm').attr('target_id');
            var url = $('#confirm').attr('url');

            $.post(url + 'ajaxdel/', { id: id },
              function(data){
                if ( data.status == true ){
                    refleshList();
                }else{
                    alert('Error ao excluir a informação');
                }
              }, 'json');

        }

        $('#confirm').jqmHide();

    });

}

$(document).ready(init);
