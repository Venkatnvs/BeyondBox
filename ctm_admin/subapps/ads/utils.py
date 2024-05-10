from .models import AdsBase

def GetAds(size):
    height = width = None
    if size:
        width,height = size.split('x')
        queryset = AdsBase.objects.filter(size__height=height, size__width=width,is_active=True).order_by('?')
        if queryset.exists():
            ad = queryset.first()
            url = ad.url
            forward = ad.forward_url
        else:
            url = f"https://dummyimage.com/{size}/808080/ffffff.png"
            forward = "/"
    else:
        queryset = AdsBase.objects.filter(is_active=True).order_by('?')
        if queryset.exists():
            ad = queryset.first()
            url = ad.url
            forward = ad.forward_url
            height = ad.size.height
            width = ad.size.width
        else:
            url = f"https://dummyimage.com/200x200/808080/ffffff.png"
            forward = "/"
            height = 200
            width = 200
    return url,forward,height,width