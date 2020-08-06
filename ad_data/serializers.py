from rest_framework import serializers
from ad_data.models import Adjust


class AdjustSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adjust
        fields = ['date',
                  'channel',
                  'country',
                  'os',
                  'impressions',
                  'clicks',
                  'installs',
                  'spend',
                  'revenue'
                  ]
