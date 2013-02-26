document.write('<div class="content">   ');
document.write('<div class="boxgrid">');
document.write('');
{% for i in videos %}
document.write('<div class="thumbbox">');
{% load miniature %}
document.write('<p class="thumb"><a href="{{ base_url }}v/{{ i.id }}" target="_blank"><img src="{{base_url}}{{ i|thumbnail:"160x120" }}" alt="" title=""  class="imagecache imagecache-thumbnail_usuario_listagem" width="87"/></a></p>');
document.write(' \n');
document.write('<p class="uname"><a href="{{ base_url }}v/{{ i.id }}" target="_blank">{{ i.get_name }}</a></p>');
document.write('');
document.write('</div>');
{% endfor %}
document.write('');
document.write('<div id="box_opcoes"> <div class="box_add"><a target="_blank" href="{{ base_url }}home/{{ channel }}/">Ver todos</a></div> </div> ');
document.write('</div>');
document.write('</div>');

