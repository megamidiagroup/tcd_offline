from django.template import Library

register = Library()
@register.inclusion_tag('templatetags/categories.html')
def show_childs( cat, allcategories):
    return {'categories' : cat['childs'], 'allcategories' : allcategories}