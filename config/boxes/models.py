from django.db import models


class Box(models.Model):
    name = models.CharField(max_length=200)
    inner_length = models.DecimalField(max_digits=10, decimal_places=2)
    inner_width = models.DecimalField(max_digits=10, decimal_places=2)
    inner_height = models.DecimalField(max_digits=10, decimal_places=2)
    max_weight = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name