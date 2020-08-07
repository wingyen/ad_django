import logging

from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from ad_data.models import Adjust
from ad_data.serializers import AdjustSerializer
from django.db.models import Sum
from django.db.models import FloatField, F


class AdjustViewSet(viewsets.ModelViewSet):
    queryset = Adjust.objects.all()
    serializer_class = AdjustSerializer
    permission_classes = [AllowAny]


def group_set(queryset):
    data = queryset \
        .values('channel', 'country') \
        .order_by('channel', 'country') \
        .annotate(impressions=Sum('impressions'), clicks=Sum('clicks')) \
        .order_by('-impressions', '-clicks')

    data = list(data)
    return data


@api_view(["GET"])
@permission_classes([AllowAny])
def use_cases(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    year = request.GET.get('year')
    month = request.GET.get('month')
    os = request.GET.get('os')
    country = request.GET.get('country')
    date = request.GET.get('date')
    cpi = request.GET.get('cpi')
    data = None
    queryset_in_date_range = None

    if date_from and date_to:
        """
        filter queryset in a date range
        """
        queryset_in_date_range = Adjust.objects.filter(date__range=[date_from, date_to])
        data = group_set(queryset_in_date_range)

    if date_to:
        """
        filter queryset before date of date_to
        """
        queryset_in_date_range = Adjust.objects.filter(date__lte=date_to)

        data = group_set(queryset_in_date_range)

    if year and month and os:
        queryset = Adjust.objects \
            .filter(date__year=year, date__month=month, os=os) \
            .values('date', 'installs') \
            .order_by('date')

        data = list(queryset)

    if country and date:
        country = country.upper()
        queryset = Adjust.objects \
            .filter(date=date, country=country) \
            .values('os') \
            .annotate(revenue=Sum('revenue')) \
            .order_by('-revenue')
        data = list(queryset)

    if country and cpi:
        country = country.upper()
        queryset = Adjust.objects.filter(country=country) \
            .values('channel') \
            .annotate(spend_sum=Sum('spend', output_field=FloatField()),
                      installs_sum=Sum('installs', output_field=FloatField())
                      ) \
            .annotate(cpi=F('spend_sum') / F('installs_sum')) \
            .order_by('-cpi')  # maybe use average to calculate cpi?

        data = list(queryset)
        # limit cpi result to 2 decimal places
        for item in data:
            item["cpi"] = "{:.2f}".format(item["cpi"])

    return JsonResponse(data=data, safe=False)
