from django import template
from perms.models import BannedUser

register = template.Library()


@register.filter(name='is_banned')
def is_banned(user):
    try:
        banned_user = BannedUser.objects.get(user=user)
        return banned_user.is_banned
    except BannedUser.DoesNotExist:
        return False
