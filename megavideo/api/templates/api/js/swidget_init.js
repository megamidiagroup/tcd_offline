var Url = {

    // public method for url encoding
    encode : function (string) {
        return escape(this._utf8_encode(string));
    },

    // public method for url decoding
    decode : function (string) {
        return this._utf8_decode(unescape(string));
    },

    // private method for UTF-8 encoding
    _utf8_encode : function (string) {
        string = string.replace(/\r\n/g,"\n");
        var utftext = "";

        for (var n = 0; n < string.length; n++) {

            var c = string.charCodeAt(n);

            if (c < 128) {
                utftext += String.fromCharCode(c);
            }
            else if((c > 127) && (c < 2048)) {
                utftext += String.fromCharCode((c >> 6) | 192);
                utftext += String.fromCharCode((c & 63) | 128);
            }
            else {
                utftext += String.fromCharCode((c >> 12) | 224);
                utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                utftext += String.fromCharCode((c & 63) | 128);
            }

        }

        return utftext;
    },

    // private method for UTF-8 decoding
    _utf8_decode : function (utftext) {
        var string = "";
        var i = 0;
        var c = c1 = c2 = 0;

        while ( i < utftext.length ) {

            c = utftext.charCodeAt(i);

            if (c < 128) {
                string += String.fromCharCode(c);
                i++;
            }
            else if((c > 191) && (c < 224)) {
                c2 = utftext.charCodeAt(i+1);
                string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
                i += 2;
            }
            else {
                c2 = utftext.charCodeAt(i+1);
                c3 = utftext.charCodeAt(i+2);
                string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
                i += 3;
            }

        }

        return string;
    }

}


function globalInit() {

	$('<link rel="stylesheet" id="css_file" type="text/css" href="{{ server_base }}/static/css/vflow_widgets.css" />').appendTo("head")

	$('#vflow_search_button').click (function() {
			var pattern = $('#vflow_search')[0].value;
            $.getJSON( '{{ server_base }}' + '/api/swidget_search?pattern=' 
                + pattern + '&jsoncallback=?', function  (data) {
                $('#vflow_result').html(data)

			

				$('.vflow_thumb').click(function() {

						var idVideo = this.getAttribute('idVideo')
                        $('#vflow_big_layer').remove()
						$('body').append('<div id="vflow_big_layer"><div id="vflow_player"/><input type="button" value="Close" id="vflow_player_close" /></div></div>')
						$('#vflow_player_close').click (function() {
							$('#vflow_big_layer').hide()
							$('#vflow_player').html('')
							})

						$('#vflow_big_layer').show()
						$('#vflow_player').html('')
						$('#vflow_player').flash( { 'src' :  '{{ server_base }}' + '/swf/player.swf?idVideo=' +  idVideo + '&amp;uri='+ '{{ server_base }}' + '/&amp;playAuto=false', 'width' : '400', 'height' : '300' })

					})
				}
	)


})

}


$(document).ready(globalInit)

