var t          = 0;
var cont       = 0;
var arr_user   = new Array();
var arr_msg    = new Array();
var arr_call   = new Array();
var arr_mantem = new Array();
var elementos  = '';
var input_text = '';
var arr_super  = new Array();
var history    = 'false';

function init()
{
    timedCount(false);
    
    $(".aba_open").click(function(e){
        var obj = $(this).parent();

        if ( obj.attr('id') == 'none' )
        {
            $.ajax({
                type: "POST",
                url: $('.ocultos').attr('load'),
                data: {action: 'open', id_user: obj.attr('id_user'), id_chat: obj.attr('id_chat'), id_video: obj.attr('id_video'), list_id_lido: '', iCodigo: $('.webchat').attr('iCodigo')},
                dataType: "script",
                success: function(r){
                    obj.css('display', 'block').attr('id', 'block').find(".conteiner").css("display", "block");
                }
            });
            return false;
        }
        
        if ( arr_user.length > 0 )
        {
            if ( obj.attr('id') == 'none' )
            {
                obj.attr('id', 'block').find(".conteiner").css("display", "block"); 
            }
            else
            {
                obj.attr('id', 'none').find(".conteiner").css("display", "none");  
            }
        }
        else
        {
            obj.attr('id', 'none').find(".conteiner").css("display", "none");
        }
    });
    
    $(".aba_close").click(function(e){
        var obj = $(this).parent();
        obj.css('display', 'none').attr('id', 'none');
        
        $.ajax({
            type: "POST",
            url: $('.ocultos').attr('load'),
            data: {action: 'close', id_user: obj.attr('id_user'), list_id_lido: '', iCodigo: $('.webchat').attr('iCodigo')},
            dataType: "script",
            success: function(r){
                
            }
        });         
    });
    
    $(".history").click(function(e){
    	$(".history").html('Aguarde...');
        timedCount(true);         
    });
     
}

function IsNumeric(n) 
{
    return !isNaN(parseFloat(n)) && isFinite(n);
}

function list_ids_lido(obj)
{
    var list_id_lido = '';
    
    obj.find(".conteiner ul li").each(function(e){
        var li = $(this);
        if ( li.attr('lido') == '0' && li.attr('class') == undefined )
        {
            var _id = li.attr('id');
            var id  = _id.split('_');
            if ( IsNumeric(id[1]) )
            {
                list_id_lido += id[1] + "-";
            }
            
            li.attr('lido', '1');
        }   
    });
    
    if ( list_id_lido != '' )
    {
        list_id_lido = list_id_lido.substring(0,(list_id_lido.length - 1));
    } 
    
    return list_id_lido;
}

function get_msg(obj)
{    
    $(obj).focus();    
    if ( $(obj).val() == '' || $(obj).val() == 'Digite aqui a mensagem' ){
        $(obj).val('');
    }
    else
    {
        $(obj).css('color', '#666');
    }
}

function get_msg_onblur(obj)
{
    $(obj).focus();
    if ( $(obj).val() == '' || $(obj).val() == $(obj).attr('title') )
    {
        $(obj).val( $(obj).attr('title') );
    }
}

function set_msg(e, obj)
{
	
    var $this = $(obj).parent().parent();

    if(e.keyCode == 13 && $(obj).val().trim().length > 0){
    	$(obj).attr('disabled', true);
    	clearTimeout(t);    
        $.ajax({
            type: "POST",
            url: $('.ocultos').attr('load'),
            data: {action: 'set_msg', id_user: $this.attr('id_user'), list_id_lido: '', id_chat: $this.attr('id_chat'), id_video: $this.attr('id_video'), mensagem: $(obj).val(), iCodigo: $('.webchat').attr('iCodigo')},
            dataType: "script",
            success: function(r){
                $(obj).attr('disabled', false);
                t = setTimeout("timedCount(false)", 3000);
                list_msg(obj);   
            }
        });

        $(obj).val(input_text);    
    }
    
    if(e.keyCode == 13){
    	e.preventDefault();
    }

}

function create_call(id_user, call)
{
    var obj;
    
    if ( $('.ocultos').length )
    {
        obj = $('.ocultos');
	}

    if (call == false)
    {
        obj.attr('id', 'block').css('display', 'block');
    }
    
    return obj;
}

function get_user(id_user)
{
    
    var obj = create_call(id_user, false);
    
    $.ajax({
        type: "POST",
        url: $('.ocultos').attr('load'),
        data: {action: 'msg', id_user: id_user, iCodigo: $('.webchat').attr('iCodigo')},
        dataType: "script",
        success: function(r){
            list_msg(obj);
        }
    });
    
}

function aba_open($this)
{
    var obj = $($this).parent();

    if ( obj.attr('id') == 'none' )
    {
        $.ajax({
            type: "POST",
            url: $('.ocultos').attr('load'),
            data: {action: 'open', id_user: obj.attr('id_user'), id_chat: obj.attr('id_video'), id_chat: obj.attr('id_video'), list_id_lido: '', iCodigo: $('.webchat').attr('iCodigo')},
            dataType: "script",
            success: function(r){
                obj.css('display', 'block').attr('id', 'block').find(".conteiner").css("display", "block");
                timedCount(false);
            }
        });
        return false;
    }

    if ( arr_user.length > 0 )
    {
        if ( obj.attr('id') == 'none' )
        {
            obj.attr('id', 'block').find(".conteiner").css("display", "block"); 
        }
        else
        {
            obj.attr('id', 'none').find(".conteiner").css("display", "none");  
        }
    }
    else
    {
        obj.attr('id', 'none').find(".conteiner").css("display", "none");
    }
    return false;
}
    
function aba_close($this)
{
    var obj = $($this).parent();
    obj.css('display', 'none').attr('id', 'none');
    
    if ( obj.hasClass('webchat-msg3') )
    {
        obj.removeClass('webchat-msg webchat-msg3').addClass('webchat-msg');
    }
    
    if ( obj.hasClass('webchat-msg2') )
    {
        obj.removeClass('webchat-msg webchat-msg2').addClass('webchat-msg');
    }
    
    if ( obj.hasClass('webchat-msg1') )
    {
        obj.removeClass('webchat-msg webchat-msg1').addClass('webchat-msg');
    }
    
    obj.clone().prependTo(".ocultos");
    obj.remove();

    $.ajax({
        type: "POST",
        url: $('.ocultos').attr('load'),
        data: {action: 'close', id_user: obj.attr('id_user'), list_id_lido: '', iCodigo: $('.webchat').attr('iCodigo')},
        dataType: "script",
        success: function(r){
            
        }
    });
    return false;         
}

function timedCount(history)
{

    clearTimeout(t);
    
    $.ajax({
        type: "POST",
        url: $('.ocultos').attr('load'),
        data: {action: '', iCodigo: $('.webchat').attr('iCodigo'), history: history, lidos:list_ids_lido($('.ocultos'))},
        dataType: "script",
        success: function(r){
        	
        	if (history == true){
        		$(".history").remove();
        	}
            
            $(".webchat .aba_open span").html(arr_user.length);
            
            $(".webchat .conteiner").css('display', $(".webchat").attr('id'));
            
            if ( arr_call.length <= 0 && arr_msg.length > 0 )
            {
                var obj = create_call(arr_msg[cont].id_user, false);
                list_msg(obj);
            }

        }
    });
    
    t = setTimeout("timedCount(false)", 3000);
    
}

function list_msg(obj)
{
	
    var welcome = '';
    var h       = 0;

    if ( String(history) == 'true' ){
    	welcome = '<li class="welcome">' + obj.find("div.msg ul li.welcome").html() + '</li><br />';
    	obj.find("div.msg ul li.welcome").remove();
        obj.find("div.msg ul").html(welcome);
    }

    for ( var c = 0; c < arr_msg.length; c++ )
    {
        
        obj = create_call(arr_msg[c].id_user, false);

        obj.css('display', 'block').attr('id_user', arr_msg[c].id_user).attr('id_chat', arr_msg[c].id_chat).attr('id_video', arr_msg[c].id_video);    

        if ( obj.find("div.msg ul li#line_" + arr_msg[c].id_chat).length < 1 )
        {
            elementos  = '';
            if ( arr_msg[c].session_user_id != arr_msg[c].id_user )
            {
                elementos += "<li id='line_" + arr_msg[c].id_chat + "' lido='0'>";
                elementos += arr_msg[c].user + ": ";
            }
            else
            { 
                elementos += "<li class='my' id='line_" + arr_msg[c].id_chat + "' lido='0'>";
                elementos += "eu: ";
            }
            elementos +=    arr_msg[c].msg;
            elementos += "</li>";

            var ul = obj.find("div.msg ul").append(elementos);

        }

    }
    
    obj.find("div.msg ul li").each(function(e){
        h += $(this).height();
    });
    
    if ( h > 135 )
    {
        obj.find("div.msg ul").css('height', '163px').css('overflow', 'auto').scrollTop(h);
    }
    else
    {
        obj.find("div.msg ul").css('height', 'auto').css('overflow', 'none');
    }

}

$(document).ready(init);