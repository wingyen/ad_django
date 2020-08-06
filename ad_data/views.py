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


@api_view(["GET"])
@permission_classes([AllowAny])
def use_cases(request):

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    date = request.GET.get('date')
    os = request.GET.get('os')
    country = request.GET.get('country')
    cpi = request.GET.get('cpi')
    data = None
    queryset_in_date_range = None

    if date_from and date_to:

        queryset_in_date_range = Adjust.objects.filter(date__range=[date_from, date_to])

        data = queryset_in_date_range \
            .values('channel', 'country') \
            .order_by('channel', 'country') \
            .annotate(impressions=Sum('impressions'), clicks=Sum('clicks')) \
            .order_by('-impressions', '-clicks')

        data = list(data)

    if date and os:
        queryset = Adjust.objects \
            .filter(date=date, os=os) \
            .values('channel', 'country', 'os', 'installs') \
            .order_by('installs')
        data = {
            date: list(queryset)
        }

    if country:
        if date:
            queryset = Adjust.objects \
                .filter(date=date) \
                .values('country', 'os') \
                .annotate(revenue=Sum('revenue')) \
                .order_by('-revenue')
            data = {
                date: list(queryset)
            }


        if queryset_in_date_range:
            queryset = queryset_in_date_range\
                .values('country', 'os') \
                .annotate(revenue=Sum('revenue')) \
                .order_by('-revenue')
            data = {
                date_from + '_' + date_to: list(queryset)
            }
    if country and cpi:
        country = country.upper()
        queryset = Adjust.objects.filter(country=country)\
            .values('channel')\
            .annotate(spend_sum=Sum('spend', output_field=FloatField()),
                      installs_sum=Sum('installs', output_field=FloatField())
                      )\
            .annotate(cpi=F('spend_sum')/F('installs_sum'))\
            .order_by('-cpi')

        data = list(queryset)

    return JsonResponse(data=data, safe=False)

