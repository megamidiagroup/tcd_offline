
function reflesh_enchance(filter){
  $('table.enhance').empty()
  $('table.enhance').before('<div class="ajax_loader"><img src="/megavideo/static/manager/images/ajax-loader.gif" border="0"> <span>Carregando ...</span></div>');
  
  $('table.enhance').load('/megavideo/manager/statistics/ajax_table/?month=' + filter, function(){
    $('.grafico .visualize').remove();
    $('table.enhance').visualize({type:'line', width:'800', style:'grap'}).trigger('visualizeRefresh');

    $('.ajax_loader').remove();

    //load another table
    $('table.enhance_domains').empty()
    $('table.enhance_domains').load('/megavideo/manager/statistics/ajax_table_domain/?month=' + filter, function(){
      $('table.enhance_domains').visualize({ width:'800', height: '200px', style:'grap' , colors:['#17447D', '#BA2C3A' , '#2CAEBB', '#3D7FAF', '#2F3B4B'] }).trigger('visualizeRefresh');
    });
    
  });
  
  
}


function init(){
    
    try {
      $(".ddselect").css("z-index", "10000").msDropDown({visibleRows:15, rowHeight:23});
      $(".ddTitle span.arrow").before('<span class="before"><img src="/megavideo/static/manager/images/combo1.png" border="0" /></span>');
      $(".ddTitle span.arrow").after('<span class="after"><img src="/megavideo/static/manager/images/combo3.png" border="0" /></span>');
    } catch(e) {
      alert("Error msDropDown: " + e);
    } 
    
    try {
        $("body select.ddselect").msDropDown();
        $(".ddTitle span.arrow").before('<span class="before"><img src="/megavideo/static/portal/images/left_bg.png" border="0" /></span>');
        $(".ddTitle span.textTitle").after('<span class="after"><img src="/megavideo/static/portal/images/right_bg.png" border="0" /></span>');
    } catch(e) {
        //alert("Error msDropDown: " + e);
    }


    if ($(".datepicker").length > 0){
        $(".datepicker").datepicker({
            changeMonth: true,
            changeYear: true
        });
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
      });
    }
    
    try{
        $('table.enhance').visualize({type:'line', width:'800', style:'grap'});
    }catch(e){
        $('body').after('<div class="erro">Erro: ' + e + '</div>');
    }

    try{
       $('table.downloads').visualize({type: 'pie', height: '150px', width: '160px', pieMargin:5 , colors:['#55a0b3','#72b8c9','#BE2424'] });
    }catch(e){
       $('body').after('<div class="erro">Erro: ' + e + '</div>');
    }

    try{
       $('table.espaco').visualize({type: 'pie', height: '150px', width: '160px', pieMargin:5 , colors:['#415877', '#778FB0', '#BE2424']  });
    }catch(e){
       $('body').after('<div class="erro">Erro: ' + e + '</div>');
    }

    try{
        $('table.enhance_domains').visualize({ width:'800', height: '200px', style:'grap' , colors:['#17447D', '#BA2C3A' , '#2CAEBB', '#3D7FAF', '#2F3B4B'] });
    }catch(e){
        $('body').after('<div class="erro">Erro: ' + e + '</div>');
    }
  
    
    $('select#speed').selectToUISlider({
      labels: 15,
      sliderOptions: {
        stop: function(e,ui) { 
          var currentValue = $('select#speed').val();
          
          reflesh_enchance(currentValue);
          
        }
      }
    }); 

    
}



function selectMaisVistos(item, url){
    window.document.location = url + $(item).val() + '/';
}

$(document).ready(init);
