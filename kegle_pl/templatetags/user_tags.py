from django import template
from django.contrib.auth.models import Group
from kegle_pl.models import Zawodnicy
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()
#filter wybierający grupy w templatce w miejscu {% load user_tags %}
# po tym można użyć lini wybierającej {% if request.user|has_group:"Zawodnicy" %} (user|grupa)
@register.filter(name='has_group')
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name)
    return group in user.groups.all()

"""Sprawdza czy zawodnik ma otwartą możliwość edycji. Przy zawodniku do 
uzupełnienia nadaje na siłę wartość 0 """
@register.filter(name='zawodnik_edycja')
def zaw_edit(user, edycja_danych):
    try:
        upraw = Zawodnicy.objects.get(user=user)
    except ObjectDoesNotExist:
        edycja_danych=0
        return edycja_danych
    return upraw.edycja_danych

@register.filter(name='ilosc')
def times(number):
    if number==1:
        return range(number)
    else:
        return range(number+1)
