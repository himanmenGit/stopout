from bs4 import BeautifulSoup
import re
import requests


class EpisodeData:

    def __init__(self, episode_id, webtoon_title, episode_num, url_thumbnail, title, rating, created_date):
        self._episode_id = episode_id
        self._webtoon_title = webtoon_title
        self._episode_num = episode_num
        self._url_thumbnail = url_thumbnail
        self._title = title
        self._rating = rating
        self._created_date = created_date

    @property
    def episode_id(self):
        return self._episode_id

    @property
    def episode_id(self):
        return self._webtoon_title

    @property
    def episode_num(self):
        return self._episode_num

    @property
    def url_thumbnail(self):
        return self._url_thumbnail
        pass

    @property
    def title(self):
        return self._title
        pass

    @property
    def rating(self):
        return self._rating

    @property
    def created_date(self):
        return self._created_date
        pass

    def __str__(self):
        return f'webtoon title: {self._webtoon_title}, ' \
               f'episode_id: {self._episode_id}, ' \
               f'episode_num: {self._episode_num}, ' \
               f'url_thumbnail: {self._url_thumbnail}, ' \
               f'title: {self._title}, ' \
               f'rating: {self._rating}, ' \
               f'created_date: {self._created_date}' \



def get_episode_list(webtoon_id, page):
    request_url = f'https://comic.naver.com/webtoon/list.nhn'
    request_params = {
        'titleId': webtoon_id,
        'page': page,
    }
    response = requests.get(request_url, request_params)

    soup = BeautifulSoup(response.text, 'lxml')
    ep_tr = soup.select('#content > table > tr')

    webtoon_title_h2 = soup.select_one('#content > div.comicinfo > div.detail > h2')
    if webtoon_title_h2:
        webtoon_title = webtoon_title_h2.contents[0].strip()

    episode_list = list()
    for ep in ep_tr:
        try:
            # 섬네일 url
            ep_thumbnail_url = ep.select_one('td > a').find('img')['src']

            td_title = ep.select_one('td.title > a')
            # href 태그의 episode_id 가져옴
            pattern = re.compile(r'.*?no=(?P<no>\d+).*', re.S)
            # href의 no를 가져옴
            ep_num = pattern.search(td_title.attrs['href']).group('no')

            # 제목
            ep_title = td_title.get_text()

            # 점수
            ep_rating = ep.select_one('div.rating_type > strong').get_text()

            # 등록일
            ep_created_date = ep.select_one('td.num').get_text()

            ep_data = EpisodeData(
                episode_id=webtoon_id,
                webtoon_title=webtoon_title,
                episode_num=ep_num,
                url_thumbnail=ep_thumbnail_url,
                title=ep_title,
                rating=ep_rating,
                created_date=ep_created_date,
            )
            episode_list.append(ep_data)
        except Exception as e:
            print(e)

    return episode_list


if __name__ == '__main__':
    episode_list = get_episode_list(20853, 1)
    for episode in episode_list:
        print(episode)
