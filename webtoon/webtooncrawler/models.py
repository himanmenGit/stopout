from django.db import models
from crawler import crawler


class Webtoon(models.Model):
    webtoon_id = models.CharField(max_length=10)
    title = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.title}'

    # 추후 웹툰 커버 url 필드 추가 예정
    # 1 화부터 들고 와서 뿌려주는 기능도 추가 해볼까
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
    created_date = models.DateField('date published')

    def __str__(self):
        return f'{self.episode_id}-{self.title}'

