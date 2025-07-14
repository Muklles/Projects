from django.db import models

class Content(models.Model):
    sequency = models.AutoField(primary_key=True)
    title = models.TextField(max_length=255)
    content = models.TextField(max_length=10000)
