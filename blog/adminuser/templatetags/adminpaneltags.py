from django import template
import json

register = template.Library()


@register.filter
def countOfList(data):
    try:
        return len(json.loads(data))
    except:
        return 0