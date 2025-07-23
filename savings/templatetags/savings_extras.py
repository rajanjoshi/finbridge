from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter
def json_chart(contributions_queryset):
    labels = [c.date.strftime('%Y-%m-%d') for c in contributions_queryset]
    data = [float(c.amount) for c in contributions_queryset]
    return mark_safe(json.dumps({'labels': labels, 'data': data}))