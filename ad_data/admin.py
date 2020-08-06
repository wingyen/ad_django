from django.contrib import admin
from ad_data.models import Adjust


class AdjustAdmin(admin.ModelAdmin):
    list_display = ['date',
                    'channel',
                    'country',
                    'os',
                    'impressions',
                    'clicks',
                    'installs',
                    'spend',
                    'revenue']


admin.site.register(Adjust, AdjustAdmin)
