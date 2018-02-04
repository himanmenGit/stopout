from django.db import models
from crawler import crawler


class Webtoon(models.Model):
    webtoon_id = models.CharField(max_length=10)
    title = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.title}'

    def get_episode_list(self):
        episode_list = crawler.get_episode_list(self.webtoon_id, 1)

        for episode in episode_list:
            if Episode.objects.filter(episode_id=episode['episode_id']).exists():
                continue

            Episode.objects.create(
                webtoon=self,
                episode_id=int(episode['episode_id']),
                title=episode['title'],
                rating=float(episode['rating']),
                created_date=episode['created_date'],
            )


class Episode(models.Model):
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE)
    episode_id = models.IntegerField(default=0)
    title = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    created_date = models.DateTimeField('date published')

    def __str__(self):
        return f'{self.episode_id}-{self.title}'

