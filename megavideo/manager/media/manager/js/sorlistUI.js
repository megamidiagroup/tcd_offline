// do stuff when DOM is ready
$(document).ready(function() {
	
	try {
        $("body select.ddselect").msDropDown();
        $(".ddTitle span.arrow").before('<span class="before"><img src="/megavideo/static/manager/images/combo1.png" border="0" /></span>');
	$(".ddTitle span.arrow").after('<span class="after"><img src="/megavideo/static/manager/images/combo3.png" border="0" /></span>');
    } catch(e) {
        //alert("Error msDropDown: " + e);
    }
	
   // do exclude with redirection
   $('.exclude').click(
      function(e){

           var msg = this.getAttribute('msg')
           var url = this.getAttribute('target')
           var id = this.getAttribute('target_id')

           response = confirm(msg);


        if(response){
            $.post(url, { id: id },
              function(data){
                if ( data.status == true ){
                    $('.line_' + id ).fadeOut();
                }else{
                    alert('Error ao excluir a informação');
                }
              },'json');

        }

   });


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
                            $("#"+id).attr('title', 'Despublicado');
                            $("#"+id).html('<img src="/megavideo/static/manager/images/bt_despublicar.gif" /> Despublicado ');
                            $(".subline_"+id).fadeOut();
                            //$(".line_"+id).fadeOut();
                            //$(".subline_"+id).fadeOut();

                        }else{
                            $('#total_active').html( parseInt($('#total_active').html()) + 1);
                            $('#total_desactive').html( parseInt($('#total_desactive').html()) - 1);
                            $("#"+id).attr('title', 'Publicado');
                            $("#"+id).html('<img src="/megavideo/static/manager/images/bt_publicar.gif"/> Publicado ');
                            //$(".line_"+id).fadeOut();
                            //$(".subline_"+id).fadeOut();

                        }

                    }else{

                        alert(data.alert)

                    }

                  },'json');

           }
   );




   $('.orderIcon').click(
           function(e){
            var url = this.getAttribute('target')
               var id  = this.getAttribute('id')

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
	           function(){
	
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
            function (){
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
            function (){
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


    $('#bt_send_category').click(function(){

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
         $.post(url, { select_category: select_category, select_video : select_video, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
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

    $('#list_video').sortable({
         axis    : "y",
         cursor  : "pointer",
         opacity :  .6,
         
         update  : function(e){
             var order = serializeLists('#list_video');
             var url   = '/megavideo/manager/orderby/ajax_video_sort/';
             
             $.post(url, { order: order, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
                function(data){
                    if (data.status == false) {
                        alert("Erro ao ordenar a série");
                    }
                  }, 'json');
             }
      });

      $('#list_subcategory').sortable({
         axis    : "y",
         cursor  : "pointer",
         opacity :  .6,

         update: function(){
             var order = serializeLists('#list_subcategory');
             var url   = '/manager/orderby/ajax_category_sort/';
             
             $.post(url, { order: order, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
                function(data){
                    if (data.status == false) {
                          alert("Erro ao ordenar a série");
                      }
              }, 'json');
          }
      });
      
      
      $('#list_category').sortable({
          axis    : "y",
          cursor  : "pointer",
          opacity :  .6,
          
          update: function(){
              var order = serializeLists('#list_category');
              var url   = '/megavideo/manager/orderby/ajax_category_sort/';

              $.post(url, { order: order, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
                 function(data){
                     if (data.status == false) {
                           alert("Erro ao ordenar a série");
                       }
               }, 'json');

           }
       });
      
      
      $('#list_category li').dblclick(function(){
		  id = $(this).attr('id');
		  $('#list_subcategory').empty();
		  $('#list_category li').removeClass('selected');
		  $(this).addClass('selected');
		  
		  var url = $("#form_list").attr("action") + 'manager/orderby/reload/';
		  
		  $.post(url, {'catid': id, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() } , 
			  function(data){
			  
				  $('#list_subcategory').html(data.content);
				  $('#list_subcategory li').dblclick(function(){
					  id = $(this).attr('id');
					  parentid = $(this).attr('parentid');
					  $('#list_subcategory li').removeClass('selected');
					  $(this).addClass('selected');
					  
					  $('#list_video').empty();
					  $('#list_video').load(url, {'subcatid':id , 'parentid': parentid });
				  });
				  
				  $('#list_video').empty();
				  $('#list_video').load(url, {'subcatid': data.subcatid , 'parentid': data.parentid  } );
				  
			  }, 
		  'json');
		  
	  });
      
      
      $('#list_subcategory li').dblclick(function(){
    	  
		  var id	   = $(this).attr('id');
		  var parentid = $(this).attr('parentid');
		  var url 	   = $("#form_list").attr("action") + 'manager/orderby/reload/';
		  
		  $('#list_subcategory li').removeClass('selected');
		  $(this).addClass('selected');
		  
		  $('#list_video').empty();
		  $('#list_video').load(url, {'subcatid':id, 'parentid' : parentid, csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() });
	  });
      

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
      
});

//post-submit callback 
function showResponse(responseText, statusText, xhr, $form)  { 
	$('#bug_return').css('display','none');
	$('#bug_return').html(responseText.msg);
    $('#bug_return').slideDown();
} 


function serializeLists(target) {
        var order = new Array();
        $(target).find('li').each(function() {
            order.push( $(this).attr('id') );
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
