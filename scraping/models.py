from django.db import models

# Create your models here.
class Platform(models.Model):
  title = models.CharField(max_length=100)
  last_scraped = models.DateField(null=True)

class Review(models.Model):
  platform = models.ForeignKey(Platform, on_delete=models.DO_NOTHING)
  date = models.DateField()
  total_rating_score = models.DecimalField(max_digits=5, decimal_places=2)
  title = models.CharField(max_length=200)
  url = models.CharField(max_length=250, null=True)

  author_status = models.BooleanField(null=True)
  author_role = models.CharField(max_length=50, null=True)
  author_location = models.CharField(max_length=50, null=True)

class Text(models.Model):
  review = models.ForeignKey(Review, on_delete=models.CASCADE)
  text_type = models.CharField(max_length=100)
  content = models.CharField(max_length=2500)

class Rating(models.Model):
  review = models.ForeignKey(Review, on_delete=models.CASCADE)
  rating_type = models.CharField(max_length=100)
  rating_score = models.DecimalField(max_digits=5, decimal_places=2)
