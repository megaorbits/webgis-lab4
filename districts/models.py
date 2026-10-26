from django.contrib.gis.db import models


class District(models.Model):
    name = models.CharField(max_length=100)
    province = models.CharField(max_length=100, null=True, blank=True)
    pcode = models.CharField(max_length=20, null=True, blank=True)
    pop_2023 = models.BigIntegerField(null=True, blank=True)
    area_km2 = models.FloatField(null=True, blank=True)
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.name
