from django.contrib.gis.db import models


class City(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField(geography=True)

    def __str__(self):
        return self.name
