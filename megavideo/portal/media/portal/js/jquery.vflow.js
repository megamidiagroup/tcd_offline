/*
 * Jquery.vflow v0.1  
 */

(function($){
  
  $.fn.vflow_embed = function( option ){
    
     var domain='http://virtual1.vflow:8010';
     option.render_to_html=1;
     this.load(domain + '/api/embed.js', option)
     
  }
  
})( jQuery );