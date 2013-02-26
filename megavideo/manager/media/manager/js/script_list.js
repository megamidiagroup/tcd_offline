function init() {

   // do exclude with redirection
   $('.exclude').click(
      function(e){

        $('#confirm').attr('url', $(this).attr('url')).attr('target_id', $(this).attr('target_id'));

           confirm($(this).attr('msg'));

        return false;

   });
   
   $('.publicado ').click(function(){
		pub_id = $(this).attr('id')
		id = pub_id.split('_')[1]
		target = $(this).attr('target')
		bk = $(this).css('background-position');
		animate = $(this);
		
		$.post(target, {'id': id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()} , function(data){
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


   $('.commentIcon').click(
           function(e){

            var url = this.getAttribute('target')
               var id  = this.getAttribute('id')

            $.post(url, { id: id },
                  function(data){

                     if(!data.alert){

                        if (data.status == false){

                            if( parseInt($('#total_active').html()) > 0 ) {
                                $('#total_active').html( parseInt($('#total_active').html()) - 1);
                            }

                            $('#total_desactive').html( parseInt($('#total_desactive').html()) + 1);
                            $("#"+id).attr('title', 'Despublicado').html('<img src="/megavideo/static/manager/images/bt_despublic.png" border="0" width="12" /> Despublicado ');

                        }else{
                            $('#total_active').html( parseInt($('#total_active').html()) + 1);

                            if( parseInt($('#total_desactive').html()) > 0 ){
                                $('#total_desactive').html( parseInt($('#total_desactive').html()) - 1);
                            }

                            $("#"+id).attr('title', 'Publicado').html('<img src="/megavideo/static/manager/images/bt_publicado.png" border="0" width="12" /> Publicado ');

                        }

                    }else{

                        alert(data.alert)

                    }

                  } , 'json');

           }
   );

   $('.orderIcon').click(
           function(e){
            var url = this.getAttribute('target')
               var id  = this.getAttribute('id')

            $.post(url, { id: id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
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

      $('img.change_status').click(
            function (e){
            bgColorRed  = 'rgb(246, 187, 189)';
            bgColorBlue = 'rgb(245, 245, 247)';
            className = $(this).attr('target');
            currentColor = $(className).css('background-color');

            var url = '/megavideo/manager/program/ajaxpublish/';

             $.post(url, { value: className, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
                  function(data){

                 if (data.published){

                    $(className).css('background-color',bgColorBlue);
                    $(className + ' img.change_status').attr('src','/megavideo/static/manager/images/bt_desativado.gif');
                    $(className + ' img.change_comment').attr('src','/megavideo/static/manager/images/comments.gif');
                    $(className + ' img.change_view').attr('src','/megavideo/static/manager/images/views.gif');

                 }else{

                    $(className).css('background-color',bgColorRed);
                      $(className + ' img.change_status').attr('src','/megavideo/static/manager/images/bt_ativado.gif');
                    $(className + ' img.change_comment').attr('src','/megavideo/static/manager/images/comments_red.gif');
                    $(className + ' img.change_view').attr('src','/megavideo/static/manager/images/views_red.gif');

                 }

              },'json');
    });

      $('img.change_status_admin').click(
            function (e){
            bgColorRed  = 'rgb(246, 187, 189)';
            bgColorBlue = 'rgb(237, 238, 242)';
            className = $(this).attr('target');
            currentColor = $(className).css('background-color');
            var url = '/megavideo/manager/program/ajaxpublish/';
             $.post(url, { value: className, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
              function(data){
                 if (data.published){
                    $(className).css('background-color',bgColorBlue);
                    $(className + ' img.change_status_admin').attr('src','/megavideo/static/manager/images/bt_desativado.gif');
                    $(className + ' img.change_comment').attr('src','/megavideo/static/manager/images/comments.gif');
                    $(className + ' img.change_view').attr('src','/megavideo/static/manager/images/views.gif');
                 }else{
                    $(className).css('background-color',bgColorRed);
                      $(className + ' img.change_status_admin').attr('src','/megavideo/static/manager/images/bt_ativado.gif');
                    $(className + ' img.change_comment').attr('src','/megavideo/static/manager/images/comments_red.gif');
                    $(className + ' img.change_view').attr('src','/megavideo/static/manager/images/views_red.gif');
                 }
              },'json');
    });

    $('#bt_send_category').click(function(e){

        select_category = Array();
        select_video = Array();

        $('input:checked').each(function(e){
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

    $('.openSubCategory').click(function(e){
        if ($("ul.openOptions" + $(this).attr("name")).css('display') == 'block'){
            $("ul.openOptions" + $(this).attr("name")).slideUp(500).css("display", 'none');
            $(this).html("<img src='/megavideo/static/manager/images/bullet_up.gif' border='0' />");
        } else {
            $("ul.openOptions" + $(this).attr("name")).slideDown(1000).css("display", 'block');
            $(this).html("<img src='/megavideo/static/manager/images/bullet_buttom.gif' border='0' />");
        }
    });


      $('#bt_categorize').click(function(e){
          $('#list_category').slideToggle("slow");
      });

    $("img.no_exclude").animate({ opacity: .3 }, 0);

    var db = $(".desabilita_btn");

    if ( db.length > 0 )
    {
        db.remove();
    }

    try {

        $('#confirm').jqm({
            overlay : 80,
            modal   : true,
            trigger : false
        });

    } catch(e){}
    //help http://dev.iceburg.net/jquery/jqModal/
    
    try {
		$(".ddselect").css("z-index", "10000").msDropDown({visibleRows:15, rowHeight:23});
		$(".ddTitle span.arrow").before('<span class="before"><img src="/megavideo/static/manager/images/combo1.png" border="0" /></span>');
		$(".ddTitle span.arrow").after('<span class="after"><img src="/megavideo/static/manager/images/combo3.png" border="0" /></span>');
	} catch(e) {
		alert("Error msDropDown: " + e);
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
    $('#bug_return').slideDown();
} 




/* ==================================== jModal ======================================== */

/* Overriding Javascript's Alert Dialog */

/*
function alert(msg) {
     $('#alert').jqmShow().find('div.jqmAlertContent').html(msg);
}
*/

function confirm(msg, callback) {

    $('#confirm').jqmShow().find('p.jqmConfirmMsg').html(msg).end();
    $('table td.sim:visible, table td.no:visible').unbind('click');
    $('table td.sim:visible, table td.no:visible').bind('click', function(e){

        if(this.id == "1"){

            var id  = $('#confirm').attr('target_id');
            var url = $('#confirm').attr('url');

            $.post(url, { id: id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
              function(data){
                if ( data.status == true ) {

                    $('.line_' + id ).fadeOut();

                    $('span#total').html(data.total);

                } else {
                    alert('Error ao excluir a informação');
                }
              }, 'json');

        }

        $('#confirm').jqmHide();

    });

}

$(document).ready(init);

function order(target, type){
	
	//var content = $('.order').html();
	//content = $(content).children('ul').addClass('sortable');
	
	var boxy =  Boxy.load( target , {
		title: "Ordernar Vídeos:", 
		modal : true ,
		draggable: false,
		afterShow: function(){
			updateOrder(type);
		} 
		});
		
	// here, we reload the saved order
	//restoreOrder();
	
} 

function serializeLists() {
    var order = new Array;
    $('.sortListUI').find('li').each(function() {
        order.push($(this).attr('id'));
    });
    return order;
}

function updateOrder(type){
	
   $('.sortListUI').sortable({
         axis: "y",
         cursor: "pointer",
         opacity: 0.7,
         update: function(){
             var order = '';
			 
			 $('.sortListUI').find('li').each(function() {
		        order += $(this).attr('id') + ',' ;
		     });
			 
             if (type == 'program'){
				 var url = '/megavideo/manager/program/order/sort/';
			 }
			 else if(type == 'category'){
			 	 var url = '/megavideo/manager/category/order/sort/';
			 }
             
			 $.post(url, { 'order' : order, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
	              function(data){
	                  if(data.status == false) alert("Erro ao ordenar a série")
	              },'json');
             }
      });
}
