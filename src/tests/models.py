from django.db import models


class ModelText(models.Model):
    name = models.CharField(max_length=255)
