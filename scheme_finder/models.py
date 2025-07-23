from django.db import models

class Scheme(models.Model):
    name = models.CharField(max_length=100)
    min_age = models.PositiveIntegerField()
    max_income = models.PositiveIntegerField()

    def __str__(self):
        return self.name
