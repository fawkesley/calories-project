from django.db import models


class Meal(models.Model):
    class Meta:
        app_label = 'meals'
        ordering = ('date', 'time')

    owner = models.ForeignKey('auth.User', related_name='meals')
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    calories = models.IntegerField()
