from django.db import models


class webtoon(models.Model):
    webtoon_id = models.CharField(max_length=10)
    title = models.CharField(max_length=50)


class Episode(models.Model):
    webtoon = models.ForeignKey(webtoon, on_delete=models.CASCADE)
    episode_id = models.IntegerField(default=0)
    title = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=2, decimal_places=2)
    created_date = models.DateTimeField('date published')
