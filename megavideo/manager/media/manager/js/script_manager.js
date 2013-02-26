// do stuff when DOM is ready
function init() {

   // do exclude with redirection
   $('.exclude').click(function(e) {
        $('#confirm').attr('url', $(this).attr('url')).attr('target_id', $(this).attr('target_id')).attr('removeOne', $(this).attr('removeOne'));
           confirm($(this).attr('msg'));
        return false;
   });
   
   if ($("#menubar").length){
		$("#menubar ul li").hover(function(e){
			var obj = $(this);
			obj.children('a').animate({width: 'show'}, 300);
		},  function () {
			var obj = $(this);
			if (!obj.hasClass('selected')){
				obj.children('a').animate({width: 'hide'}, 300);
			}
		});
	}

   $('.commentIcon').click(
           function(e){

            var url = this.getAttribute('target')
               var id  = this.getAttribute('id')

            $.post(url, { id: id },
                  function(data){

                     if(!data.alert){

                        if (data.status == false){
                            $('#total_active').html( parseInt($('#total_active').html()) - 1);
                            $('#total_desactive').html( parseInt($('#total_desactive').html()) + 1);
                            $("#"+id).attr('title', 'Despublicado').html('<img src="/megavideo/static/manager/images/bt_despublic.png" />');
                            $(".subline_"+id).fadeOut();
                        } else {
                            $('#total_active').html( parseInt($('#total_active').html()) + 1);
                            $('#total_desactive').html( parseInt($('#total_desactive').html()) - 1);
                            $("#"+id).attr('title', 'Publicado').html('<img src="/megavideo/static/manager/images/bt_publicado.png"/>');
                        }

                    } else {

                        alert(data.alert)

                    }

                  },'json');

           }
   );

   $('.orderIcon').click(
           function(e){
            var url = this.getAttribute('target');
            var id  = this.getAttribute('id');

            $.post(url, { id: id },
                  function(data){
                    if (data.status == false){
                        $("#"+id).attr('title', 'Despublicado');
                    }else{
                        $("#"+id).attr('title', 'Publicado');
                    }
                  },'json');

           }
   );

   $('#bt_select_all').click(
           function(e){

               if($(this).attr('title') == 'checkall'){
                   $(this).attr('title','nocheckall');
                   $("input[type='checkbox']").attr('checked', false);
               }else{
                   $(this).attr('title','checkall');
                   $("input[type='checkbox']").attr('checked', true);
               }

         }
   );
   

    $('#bt_send_category').click(function(e){

        select_category = Array();
        select_video = Array();

        $('input:checked').each(function(){
            if ($(this).attr('name') == 'category_selected') {
                select_category.push($(this).val());
            }

            if ($(this).attr('name') == 'check_video') {
                select_video.push($(this).val());
            }
        });

        var url = '/megavideo/manager/program/ajaxcategorize/';
         $.post(url, { select_category: select_category , select_video : select_video  },
            function(data){
                  if(data.status){
                      $('#list_category').slideToggle("slow");
                      alert('Categorias adicionadas com sucesso');
                  }else{
                      alert('Erro ao cadastrar as categorias tente novamente mais tarde');
                  }
            },'json');

    });

	$('#bt_categorize').click(function(){
		$('#list_category').slideToggle("slow");
	});

    jModal();
    //help http://dev.iceburg.net/jquery/jqModal/

    $("select#category_id").change(function(e){
        var id = $(this).val();
        window.document.location = $(this).attr("class") + id;
    });
	
	if ($("td.list_job").length > 0) {
		
		var base_url = $("td.list_job").attr("url");
		
		//clearInterval(headline_interval);
		var idInterval = setInterval(function(e){
			functionInterval(base_url);
		}, 8000);

	}
	
	//inoca refleshList;
	refleshList();
	
    if ($('input:checkbox').lenght) {
        $('input:checkbox').checkbox().click(function(e){
            publishVideo($(this).is(":checked"), $(this).attr("value"));
        });
    }
	
 	$('.list_img').hover(function () {
	 	$(this).find('div.caption').stop().fadeTo('normal', 1);
	 }, function () {
	 	$(this).find('div.caption').stop().fadeTo('normal', 0);
	 }); 
 	
 	$('.publicado ').click(function(){
 		pub_id = $(this).attr('id')
 		id = pub_id.split('_')[1]
 		target = $(this).attr('target')
 		bk = $(this).css('background-position');
 		animate = $(this) 
 		
 		$.post(target, {'id': id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()}, function(data){
 			if(data.status){
 				animate.stop().animate(
 		 				{backgroundPosition:"(0px 0px)"}, 
 		 				{duration:500});
 			}else{
 				animate.stop().animate(
 		 				{backgroundPosition:"(-41px 0px)"}, 
 		 				{duration:500});
 			}
 		})
 		
 	});
 
 	try {
		$(".ddselect").css("z-index", "10000").msDropDown({visibleRows:15, rowHeight:23});
		$(".ddTitle span.arrow").before('<span class="before"><img src="/megavideo/static/manager/images/combo1.png" border="0" /></span>');
		$(".ddTitle span.arrow").after('<span class="after"><img src="/megavideo/static/manager/images/combo3.png" border="0" /></span>');
	} catch(e) {
		//alert("Error msDropDown: " + e);
	} 
 
	
	if ($('.sendbug').length){
		var options = { 
	        target:        '#bug_return',   // target element(s) to be updated with server response 
	        success:       showResponse, // post-submit callback 
	        dataType:  'json',           // 'xml', 'script', or 'json' (expected server response type)
	        clearForm: true 
	    }; 
	    // bind form using 'ajaxForm' 
	    $('.sendbug').ajaxForm(options); 
	}
	
	
}

//post-submit callback 
function showResponse(responseText, statusText, xhr, $form)  { 
	$('#bug_return').css('display','none');
	
	$('#bug_return').html(responseText.msg);
	if (responseText.status == 1){
  	  $('#bug_return').css('background-color','#A80000');
	}else{
	    $('#bug_return').css('background-color','#28A11B');
	}
	
  $('#bug_return').slideDown();
} 

function publishVideo(bool, video_id){
	var url = '/megavideo/manager/program/ajaxpublish/';
	$.post(url, { video_id : video_id },
		function(data){
			if (data.error != "0"){
				alert("Não foi possivel publicar esse video!");
			}
		}, 
	'json');
}

function refleshList(){
	
	//element tooltip
	//http://craigsworks.com/projects/simpletip/
	$(".tip").each(function(e){
	
		if ( ! $(this).attr("content")){
			alert("tooltip faled : " + $(this).html() + "Não possue element content");
			return false;
		}
		
		$(this).simpletip({
			content : $(this).attr("content"),
			offset : [10, 10],
			fixed : false,
			showEffect : 'none',
			hideEffect : 'none'
		});
		
	}); 
	
}

function functionInterval(base_url){

	$("td.list_job").load(base_url, {csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()}, function(){
		refleshList();
	});

}

function ajaxdeljob(url, idjob){
	
	$.post(url, { idjob: idjob, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
		function(data){
			var base_url = $("td.list_job").attr("url");
			functionInterval(base_url);
			if (data.status == false) {
				alert("Ops, erro ao deletar o job " + idjob);
			}
		},
	'json');
	
}

function selectionCategory(item){
    window.document.location = $(item).attr("class") + item.value + '/';
}


function serializeLists() {
        var order = new Array;
        $('.sortListUI').find('li').each(function() {
            order.push($(this).attr('id'));
        });
        return order;
}


function order_program(order, id){
        var order = order;
        var id = id;
        var url = '/megavideo/manager/program/order/sort/';

        $.post(url, { order: order, id:id },
              function(data){
                  if (data.status == false) {
				  	alert("Erro ao ordenar a série");
				  }
              },'json');

}

function order_move_program(order, id , move){
        var order = order;
        var id = id;
        var url = '/megavideo/manager/program/order/'+ move +'/';

        var curr = $('li.line_'+id);

        var next = $('.line_'+id).next().html();
        var prev = $('.line_'+id).prev().html();
}

/* ==================================== jModal ======================================== */

/* Overriding Javascript's Alert Dialog */

function confirm(msg, callback) {

    $('#confirm').jqmShow().find('p.jqmConfirmMsg').html(msg).end();
    $('table td.sim:visible, table td.no:visible').unbind('click');
    $('table td.sim:visible, table td.no:visible').bind('click', function(e){

        if(this.id == "1"){

            var id  = $('#confirm').attr('target_id');
            var url = $('#confirm').attr('url');
            var removeOne = $('#confirm').attr('removeOne');

            $.post(url, { id: id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
              function(data){
                if ( data.status == true ) {

                    $('.line_' + id ).fadeOut();
                    
                    if (removeOne){
                    	remove = parseInt( $('.' + removeOne).html() );
                    	if (remove > 0){
                    		remove -= 1
                    	}
                    	$('.' + removeOne).html(remove);
                    }
                    
                    

                    $('span#total').html(data.total);
                    $('span#total_active').html(data.total_active);
                    $('span#total_desactive').html(data.total_desactive);

                } else {
                    alert('Error ao excluir a informação');
                }
              }, 'json');

        }

        $('#confirm').jqmHide();

    });

}

function confirm_categoria(msg, callback) {

    $('#confirm_categoria').jqmShow().find('p.jqmConfirmMsg').html(msg).end();
    $('#confirm_categoria :button:visible').unbind('click');
    $('#confirm_categoria :button:visible').bind('click', function(e){

        if (this.id == "1") {

            window.document.location = $('#confirm_categoria').attr('url');

        }

        $('#confirm_categoria').jqmHide();

    });

}

function jModal(){

    try {

        $('#confirm').jqm({
            overlay : 80,
            modal   : true,
            trigger : false
        });

        $('#confirm_categoria').jqm({
            overlay : 50,
            modal   : false,
            trigger : false
        });
    } catch(e){}

}


function esqueciMinhaSenha(){
	var createpass = $('#createpass').val();
	
	if (createpass == 1){
		$('#createpass').val(0);	
	}else{
		$('#createpass').val(1);
	}
	
	$('#esqueciMinhaSenha').slideToggle();
	
}

$(document).ready(init);


function serializeLists() {
        var order = new Array;
        $('.sortListUI').find('li').each(function() {
                        order.push($(this).attr('id'));
                        });
        return order;
}

function order_program(order, id){
        var order = order;
        var id = id;
        var url = '/megavideo/manager/program/order/sort/';

        $.post(url, { order: order, id:id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
                        function(data){
                        if(data.status == false) alert("Erro ao ordenar a série")
                        },'json');

}

function order_move_program(order, id , move){
        var order = order;
        var id = id;
        var url = '/megavideo/manager/program/order/'+ move +'/';

        var curr = $('li.line_'+id);

        var next = $('.line_'+id).next().html();
        var prev = $('.line_'+id).prev().html();

}

