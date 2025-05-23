from django.db import models

class CounselingCenter(models.Model):
    region = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.region})"
