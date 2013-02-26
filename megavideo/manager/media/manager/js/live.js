function init(){
	
	if ($("#playerFlash").length > 0) {

        var so = new SWFObject("{{STATIC_URL}}/static/manager/swf/rec_live.swf", "playerAoVivo", "388", "309", "9.0.0");
        so.addVariable("base_url"  , 'http://vflow.tv/');
        so.addVariable("upstreamUrl" , 'rtmp://vflow.tv/vflowopen');
        so.write("playerFlash");

	}

}



$(document).ready(init);