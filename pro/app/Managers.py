from django.db import models

class MyManager(models.Manager):
    def get_product(self, p1, p2):
        return super().get_queryset().filter(discountedprice__range=(p1, p2))
    