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
            created_td = ep.select_one('td.num').get_text()
            date_re = re.compile(
                r'(?P<year>\d{4})[-.](?P<month>\d{1,2})[-.](?P<day>\d{1,2})$'
            )
            date = date_re.search(created_td)

            # RuntimeWarning남 2018-00-00 00:00 을 DateTimeField로 바꾸는 방법?
            ep_created_date = f"{date.group('year')}-{date.group('month')}-{date.group('day')}"

            episode_list.append({
                'episode_id': ep_num,
                'url_thumbnail': ep_thumbnail_url,
                'title': ep_title,
                'rating': ep_rating,
                'created_date': ep_created_date,
            })
        except Exception as e:
            print(e)

    return episode_list
