from django import template
from ctm_admin.subapps.ads.utils import GetAds
from django.template.loader import render_to_string

register = template.Library()

@register.filter
def GetAd_size(value, arg):
    url,forward,H,W = GetAds(arg)
    html_send = render_to_string('ads_snippets/ctm_size_ads.html', {'url': url, 'forward': forward, 'H': H, 'W': W, 'size':arg})
#     html_send = f"""<div style="position: relative;width: auto;display: inline-block;box-sizing: border-box;">
# <span style="position:absolute;bottom:0;padding: 2px; background-color: #000000ba; color: #fff; z-index: 9;border-top-right-radius: 3px;">ad</span>
# <img style="max-width:100%!important;height: 100%;width:{W}px;max-height:{H}px;cursor: pointer;" onclick="window.open('{forward}', '_blank')" class="img_fluid" src="{url}" alt="ad_{arg}">
# </div>"""
    return html_send

@register.filter(name='has_permissions')
def has_permissions(user, permissions_str):
    permissions = permissions_str.split(',')
    if user.is_superuser:
        return True
    elif permissions and user.user_type and user.is_staff:
        return all(
            user.user_type.permissions.filter(
                content_type__app_label=permission.split('.')[0],
                codename=permission.split('.')[1]
            ).exists()
            for permission in permissions
        )
    else:
        return False

@register.filter(name='has_permissions_or')
def has_permissions_or(user, permissions_str):
    permissions = permissions_str.split(',')
    if user.is_superuser:
        return True
    elif permissions and user.user_type:
        return any(
            user.user_type.permissions.filter(
                content_type__app_label=permission.split('.')[0],
                codename=permission.split('.')[1]
            ).exists()
            for permission in permissions
        )
    else:
        return False
