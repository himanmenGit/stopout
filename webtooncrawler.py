from bs4 import BeautifulSoup
import re
import requests


class EpisodeData:

    def __init__(self, episode_id, episode_num, url_thumbnail, title, rating, created_date):
        self._episode_id = episode_id
        self._episode_num = episode_num
        self._url_thumbnail = url_thumbnail
        self._title = title
        self._rating = rating
        self._created_date = created_date

    @property
    def episode_id(self):
        return self._episode_id

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
        return f'episode_id: {self._episode_id}, ' \
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
    episode_list = list()
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
            ep_created_date = created_td.get_text()

        ep_data = EpisodeData(
            episode_id=webtoon_id,
            episode_num=ep_num,
            url_thumbnail=ep_thumbnail_url,
            title=ep_title,
            rating=ep_rating,
            created_date=ep_created_date,
        )
        episode_list.append(ep_data)

    return episode_list


if __name__ == '__main__':
    episode_list = get_episode_list(703835, 1)
    for episode in episode_list:
        print(episode)
