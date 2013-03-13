var mobile;

$(document).ready(function() {
	
	// para proteger ie6
	if ($.browser.msie == true && $.browser.version <= 6){
		var url = $(".no-ie6").attr("url");
		$(".no-ie6").load(url + "noie6/");
	}

	//adiciona o placeholder em browsers que não tem suporte
	Modernizr.load([{
		test : Modernizr.input.placeholder,
		nope : 'assets/js/_pf_placeholder.js'
	}]);
	
	var buttom = $('.btn_logout');
	
	buttom.attr('onclick', 'if (confirm("Deseja sair do sistema?")){window.location="' + buttom.attr('href') + '";}');
	buttom.attr('href', 'javascript:void(0);');
	
	$('.lista.categoria').find('li:last').addClass('last');
	
	//MOBILE
	var _verifyMobile = function() {
		var windowWidth = $(window).width();
		if (windowWidth < 640) {
			_mobileActions();
			mobile = true;
			return true;
		} else {
			_desktopActions();
			mobile = false;
			return false;
		}
	}
	
	var _desktopActions = function() {
		$('#main.home #content .wrapper #nav').remove();
		$('#content .wrapper .planos #nav_planos').remove();
	}
	
	var _mobileActions = function() {
		$('#main.home #content').find('.column').css('z-index', '1').filter(':first').css('z-index', '10');
		if ($('#nav').size() == 0) {
			$('#main.home #content .wrapper').append('<div id="nav"><a class="button prev" href="#">Prev</a><a class="button next" href="#">Next</a></div>');
		}

		var homeColCount = 0;
		var homeColTotal = $('#main.home #content').find('.column').size();
		$('#nav .button').live('click', function(e) {
			e.preventDefault();
			var $this = $(this);
			if ($this.is('.prev')) {
				homeColCount = homeColCount - 1;
				if (homeColCount < 0) {
					homeColCount = homeColTotal - 1;
				}
			} else if ($this.is('.next')) {
				homeColCount = homeColCount + 1;
				if (homeColCount > (homeColTotal - 1)) {
					homeColCount = 0;
				}
			}
			$('#main.home #content').find('.column').css('z-index', '1').filter(':eq(' + homeColCount + ')').css('z-index', '10');
		});

		if ($('#nav_planos').size() == 0) {
			$('#content .wrapper .planos').append('<div id="nav_planos"><a class="button prev centro" href="#">Prev</a><a class="button next centro" href="#">Next</a></div>');
		}

		$('#nav_planos .button').live('click', function(e) {
			e.preventDefault();
			var $this = $(this);
			if ($this.is('.prev.centro')) {
				$('#nav_planos .button').removeClass('centro').addClass('esquerdo');
				$('.planos .plano').removeClass('ativo');
				$('.planos .plano.esquerda').addClass('ativo');
			}

			if ($this.is('.next.centro')) {
				$('#nav_planos .button').removeClass('centro').addClass('direito');
				$('.planos .plano').removeClass('ativo');
				$('.planos .plano.direita').addClass('ativo');
			}

			if ($this.is('.next.esquerdo')) {
				$('#nav_planos .button').removeClass('esquerdo').addClass('centro');
				$('.planos .plano').removeClass('ativo');
			}

			if ($this.is('.prev.direito')) {
				$('#nav_planos .button').removeClass('direito').addClass('centro');
				$('.planos .plano').removeClass('ativo');
			}
		});
	}

	_verifyMobile();
	
	$(window).resize(function() {
		_verifyMobile();
		if($("#video").length)updatePlayer($("#video").width(), $("#video").height());
	});
	
	if($("#video").length)updatePlayer($("#video").width(), $("#video").height());
	
	if( $('.btn').length )
	{
		$('.btn').each(function(e){
			var obj1  = $(this);
			var link1 = obj1.attr('link');
			obj1.css('cursor', 'pointer').click(function(e){
				window.location = link1;
			});
		});
	}
	
	if( $('.btn-parent').length )
	{
		$('.btn-parent').each(function(e){
			var obj2  = $(this);
			var link2 = obj2.attr('link');
			obj2.parent().css('cursor', 'pointer').click(function(e){
				window.location = link2;
			});
		});
	}

});