
document.write('<div class="vflow_widget_content"> VFlow Widget <br/>');

{% for  i in videos %}
document.write('<div class="vflow_widget_line" style="width: 200px;"><a href="{{i.tv_url}}">');
document.write('<img class="vflow_widget_thumb" width="80" src="{{base_url}}{{ i.thumb }}" /> </a><div class="vflow_widget_metas"><b>{{ i.metas.nome }}</b> <br/>{{ i.metas.descricao }}</div></div>');
{% endfor %}

document.write('</div>');

