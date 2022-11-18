from django.db import models

class Image(models.Model):
    image_id = models.CharField(max_length=72)
    tags = models.CharField(max_length=255)
    size = models.CharField(max_length=70)
    created_at = models.DateTimeField()
    host = models.CharField(max_length=255)