from django.db import models


class ProductionCompany(models.Model):
    name = models.CharField(max_length=255)


class Film(models.Model):
    cache = models.FloatField(null=True)
    company = models.ForeignKey(
        ProductionCompany, on_delete=models.CASCADE, null=True, related_name="films"
    )
