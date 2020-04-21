from django.http import HttpResponse, JsonResponse

import requests
from bs4 import BeautifulSoup
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "csecrawler.settings")
import django
django.setup()

from notice_data.models import NoticeData


notice_base = 'https://computer.cnu.ac.kr/computer/notice/project.do'
notice_board = '?mode=list&&articleLimit=10&article.offset='

notice_dict = dict()


def fetch_cse_notices():
    notice_selector = 'tr > td.b-td-left > div > a'

    j = 0
    for i in range(3):
        offset = 10 * i
        req = requests.get(notice_base + notice_board + str(offset))
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        notices = soup.select(notice_selector)

        for notice in notices:
            notice_post = notice.get('href')
            notice_link = notice_base + notice_post
            print(notice_link)

            req = requests.get(notice_link)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            notice_title = soup.find('td', {'class': 'b-title-box b-no-right'}).text
            notice_text = soup.find('pre', {'class': 'pre'}).text
            notice_dict[j] = {
                'link' : notice_link,
                'title': notice_title,
                'text': notice_text
            }
            j += 1

    return notice_dict


def add_new_items(crawled_items):
    for key, val in crawled_items.items():
        NoticeData(link=val['link'], title=val['title'], text=val['text']).save()


if __name__=='__main__':
    fetched_data = fetch_cse_notices()
    print('data fetched')
    add_new_items(fetched_data)
    print('data saved')