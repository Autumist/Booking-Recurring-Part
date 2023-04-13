from django.db import models


class Testz(models.Model):
    date_string = models.DateTimeField(null=True, blank=True)
    recur_check = models.BooleanField(null=True, blank=True)
    start_date_string_array = models.CharField(
        max_length=8000, null=True, blank=True)
    end_date_string_array = models.CharField(
        max_length=8000, null=True, blank=True)
