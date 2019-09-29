from django import template
from django.contrib.auth.models import Group

register = template.Library()
#filter wybierający grupy w templatce w miejscu {% load user_tags %}
# po tym można użyć lini wybierającej {% if request.user|has_group:"Zawodnicy" %} (user|grupa)
@register.filter(name='has_group')
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name)
    return group in user.groups.all()

@register.filter(name='ilosc')
def times(number):
    if number==1:
      return range(number)
    else:
      return range(number+1)
