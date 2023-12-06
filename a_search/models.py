from django.db import models

# Create your models here.
class MagnetLink(models.Model):
    magnetName = models.CharField(max_length=200)
    magnetUrl = models.CharField(max_length=400)
    def __str__(self):
        return self.magnetName+":"+self.magnetUrl
    