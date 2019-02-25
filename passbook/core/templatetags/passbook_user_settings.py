"""passbook user settings template tags"""

from django import template

from passbook.core.models import Factor

register = template.Library()

@register.simple_tag(takes_context=True)
def user_factors(context):
    """Return list of all factors which apply to user"""
    user = context.get('request').user
    _all_factors = Factor.objects.filter(enabled=True).order_by('order').select_subclasses()
    matching_factors = []
    for factor in _all_factors:
        _link = factor.has_user_settings()
        if factor.passes(user) and _link:
            matching_factors.append(_link)
    return matching_factors