from django.db import models
from django_countries.fields import CountryField


class Adjust(models.Model):
    class Meta:
        ordering = ('date', )

    date = models.DateField()
    channel = models.CharField(max_length=100)
    country = CountryField()
    os = models.CharField(max_length=100)
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    installs = models.IntegerField()
    spend = models.DecimalField(decimal_places=2, max_digits=10)
    revenue = models.DecimalField(decimal_places=2, max_digits=10)
