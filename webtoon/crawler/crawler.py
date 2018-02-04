from bs4 import BeautifulSoup
import re
import requests


def get_episode_list(webtoon_id, page):
    request_url = f'https://comic.naver.com/webtoon/list.nhn'
    request_params = {
        'titleId': webtoon_id,
        'page': page,
    }
    response = requests.get(request_url, request_params)

    episode_list = list()

    soup = BeautifulSoup(response.text, 'lxml')
    ep_tr = soup.select('#content > table > tr')

    for ep in ep_tr:
        ep_id = None
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
            ep_id = a_href.group('no')

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

            # RuntimeWarning남 2018-00-00 00:00 을 DateTimeField로 바꾸는 방법?
            ep_created_date = f"{date.group('year')}-{date.group('month')}-{date.group('day')} 00:00"

        episode_list.append({
            'episode_id': ep_id,
            'url_thumbnail': ep_thumbnail_url,
            'title': ep_title,
            'rating': ep_rating,
            'created_date': ep_created_date,
        })

    return episode_list
