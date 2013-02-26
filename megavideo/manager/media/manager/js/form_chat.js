function init() {
	s = true;
	
	//var intervalo = setInterval("document.getElementById('content_chat').scrollTop = 1000000;", 5000);
	
    $(window).bind("unload", function() {
		var user_id = $('#user_id').val();
		if (forceLogout) {
			$.ajax({
				async: false,
				cache: false,
				type: "POST",
				url: "/chat/exit/",
				data: ({
					user_id : user_id
				}),
				success: function(response) {
				$('#name_ajax').empty();
				window.location.href='/manager/live/'
				}
			});
		}
	});
	
	var e = setInterval(function(msg) {
		// reload page
//		$('#ajax_list').load('/chat/ajax_add/')
		if (s == true) {
			$.get('/chat/ajax_add/', function (data) {
				$('#ajax_list').append(data);
				$('#content_chat').animate({scrollTop: 1000000}, 10000);
			})
		}
		else {
			$.get('/chat/ajax_add/', function (data) {
				$('#connected').load('/chat/connected/')
				$('#ajax_list').append(data);
			})
		}
	}, 2000)

}

function inicial(nickname, color) {
	
	
	// alert(e.keyCode);
	if (nickname != '') {
		$.ajax( {
			type : "POST",
			url : "/chat/nickname_manager/",
			data : {
				nickname : nickname,
				color : color
			},
			dataType : 'html',
			success : function(retornoHtml) {
				// reload page
				$('#playerFlashPrev').empty();
				$('#campos_login').empty();
				$('#nickname').val('');
				$('#name_ajax').html(retornoHtml)
				$('#connected').load('/chat/connected/')
				$("#name_ajax").css("background", "url('../images/bg_chat.jpg') no-repeat");
				$('#ajax_list').load('/chat/ajax/')
				var so = new SWFObject("{{STATIC_URL}}/static/manager/swf/rec_live.swf", "playerAoVivo", "388", "309", "9.0.0");
			        so.addVariable("base_url"  , 'http://vflow.tv/');
			        so.addVariable("upstreamUrl" , 'rtmp://vflow.tv/vflowopen');
			        so.write("playerFlash");
			        mensage();
				$('#content_chat').bind('mouseover', function(e){
					$('#content_chat').stop();
					s = false;
				});
			}

		});
	}	
	
}

var forceLogout = true;
function set_color(color, obj){
	
	var obj = $(obj);
	
	obj.parent().find('a').each(function(e){
		$(this).find('img').attr('border', '0');
	});
	
	obj.find('img').attr('border', '1');
	
	$("input[name=color]").val(color);
	$("#nickname").css('color', color);
	
}

function set_login_buttom(id){
	
	var nickname = $('input' + id).val().trim();
	var color    = $('input[name=color]').val();

	inicial(nickname, color);
	
}

function set_login_enter(e, obj){
	
	var color = $('input[name=color]').val();
	
	if (e.keyCode == 13) {
		var nickname = $(obj).val().trim();
		inicial(nickname, color);
	}
}

	
	$('.focus').focus();

function mensage() {

	$('#msg').keyup(function(e) {
		if (e.keyCode == 13) {
			envia_msg();
		}
	});

	$('#enviar_ajax').click(function() {
		envia_msg();
	});
	$("#logout_ajax").bind("click", function() {
		var user_id = $('#user_id').val().trim();
		if (forceLogout) {
			$.ajax({
				async: false,
				cache: false,
				type: "POST",
				url: "/chat/exit/",
				data: ({
					user_id : user_id
				}),
				success: function(response) {
				$('#name_ajax').empty();
				window.location.href='/manager/live/'
				}
			});
		}
	});
}
	
function envia_msg(e) {
	var msg = $('#msg').val().trim();
	var user_id = $('#user_id').val();

	// alert(e.keyCode);
		$.ajax( {
			type : "POST",
			url : "/chat/ajax_add/",
			data : {
				msg : msg,
				user_id : user_id,
			},
			dataType : 'html',
			success : function(msg) {
				// reload page
				$('#msg').val('');
				//recarrega a página por get
//             $('#ajax_list').load('/chat/ajax_add/')
				//$.get('/chat/ajax_add/', function (data) {
				//	$('#ajax_list').append(data)
				//});
				s = true;
			}
		});

	
}

$(document).ready(init);
