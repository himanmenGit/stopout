from django.db import models
from bs4 import BeautifulSoup
import requests
import re

from django.utils import timezone


class Webtoon(models.Model):
    webtoon_id = models.CharField(max_length=10)
    title = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.title}'

    def get_episode_list(self):
        request_url = f'https://comic.naver.com/webtoon/list.nhn'
        request_params = {
            'titleId': self.webtoon_id,
            'page': 1,
        }
        response = requests.get(request_url, request_params)

        soup = BeautifulSoup(response.text, 'lxml')
        ep_tr = soup.select('#content > table > tr')

        for ep in ep_tr:
            ep_num = None
            ep_thumbnail_url = None
            ep_title = None
            ep_rating = None
            ep_created_date = None

            # td 태그의 a태그
            id_td_a = ep.select_one('td:nth-of-type(1) > a')

            # href 태그의 episode_id 가져옴
            pattern = re.compile(r'.*?no=(?P<no>\d+).*', re.S)
            # href의 no를 가져옴
            a_href = pattern.search(id_td_a.attrs['href'])
            if a_href:
                ep_num = a_href.group('no')

            if Episode.objects.filter(episode_id=ep_num).exists():
                print(ep_title)
                continue

            # 섬네일 url
            thumbnail_url = id_td_a.find('img')['src']
            if thumbnail_url:
                ep_thumbnail_url = thumbnail_url

            # 제목
            title_td_a = ep.select_one('td:nth-of-type(2) > a')
            if title_td_a:
                ep_title = title_td_a.get_text()

            # 점수
            rating_td = ep.select_one('td:nth-of-type(3) > div > strong')
            if rating_td:
                ep_rating = rating_td.get_text()

            # 등록일
            created_td = ep.select_one('td:nth-of-type(4)')
            if created_td:
                date_re = re.compile(
                    r'(?P<year>\d{4})[-.](?P<month>\d{1,2})[-.](?P<day>\d{1,2})$'
                )
                date = date_re.search(created_td.get_text())

                ep_created_date = f"{date.group('year')}-{date.group('month')}-{date.group('day')} 00:00"

            Episode.objects.create(
                webtoon=self,
                episode_id=int(ep_num),
                title=ep_title,
                rating=float(ep_rating),
                created_date=ep_created_date,
            )


class Episode(models.Model):
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE)
    episode_id = models.IntegerField(default=0)
    title = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    created_date = models.DateTimeField('date published')

    def __str__(self):
        return f'{self.episode_id}-{self.title}'

# In [1]: from webtooncrawler.models import Webtoon
#
# In [2]: w = Webtoon.objects.first()
#
# In [3]: w.get_episode_list()
#
# In [4]: w.episode_set.all()
# Out[4]: <QuerySet [<Episode: 12-몫>, <Episode: 11-다정함>, <Episode: 10-이해>, <Episode: 9-신호>, <Episode: 8-온도>, <Episode: 7-제자리걸음>, <Epissode: 5-묘연>, <Episode: 4-속울음>, <Episode: 3-가치와 가격>]>
