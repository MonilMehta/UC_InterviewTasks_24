from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    plot= models.TextField()
    type = models.CharField(max_length=20)
    poster = models.ImageField(upload_to='posters/')
    searched=models.IntegerField(default=0)
    box_office = models.IntegerField()
    rating = models.FloatField()

    def __str__(self):
        return self.title