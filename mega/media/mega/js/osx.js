jQuery(function ($) {
	var OSX = {
		container: null,
		init: function () {
			var size = ( $(window).height() / 2 ) - 120;
			$("#osx-modal-content").modal({
				overlayId: 'osx-overlay',
				containerId: 'osx-container',
				closeHTML: null,
				minHeight: 80,
				autoResize: true,
				escClose: false,
				zIndex: 10000,
				opacity: 20, 
				position: [size, ],
				overlayClose: false,
				onOpen: OSX.open,
				onClose: OSX.close
			});
		},
		open: function (d) {
			var self = this;
			self.container = d.container[0];
			d.overlay.fadeIn('slow', function () {
				$("#osx-modal-content", self.container).show();
				d.container.slideDown('slow', function () {
					setTimeout(function () {
						$(".popup", self.container).show();
						$(".popup input, .popup a", self.container).fadeIn(200);
					}, 300);
				});
			})
		},
		close: function (d) {
			var self = this; // this = SimpleModal object
			d.container.animate(
				{top:"-" + (d.container.height() + 20)},
				500,
				function () {
					self.close(); // or $.modal.close();
				}
			);
		}
	};

	if ($('#osx-modal-content').length){
		
		OSX.init();

		$(window).resize(function() {
			onresizeosx();
		});
		
		onresizeosx();

	}

});

function onresizeosx()
{
	$('#osx-container').css('height', 'auto');
	$('#osx-container .popup').css('width', $('#osx-container').css('width').split('p')[0] - 30);
}
