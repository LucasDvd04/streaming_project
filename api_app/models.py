# models.py
from django.db import models

class ImportOffset(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.key}: {self.value}'
