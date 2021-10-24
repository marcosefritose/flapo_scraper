from django.db import models

# Create your models here.
class Platform(models.Model):
  title = models.CharField(max_length=100)
  last_scraped = models.DateField(null=True)

class Review(models.Model):
  platform = models.ForeignKey(Platform, on_delete=models.DO_NOTHING)
  date = models.CharField(max_length=50)
  rating = models.DecimalField(max_digits=10, decimal_places=2)
  title = models.CharField(max_length=200)
  content = models.CharField(max_length=5000)
  url = models.CharField(max_length=200)

  author_status = models.CharField(max_length=50)
  author_role = models.CharField(max_length=50)
  author_location = models.CharField(max_length=50)