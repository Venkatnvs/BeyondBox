from django.db.models import Count
from django.db.models.functions import TruncMonth
from accounts.models import UserProfile

def chart_view():
    country_data = UserProfile.objects.exclude(user__is_superuser=True).values('country').annotate(count=Count('id'))
    monthly_data = UserProfile.objects.exclude(user__is_superuser=True).annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id'))

    country_data_list = list(country_data)
    monthly_data_list = list(monthly_data)

    return country_data_list,monthly_data_list