from django.http import HttpResponse, JsonResponse

import requests
from bs4 import BeautifulSoup
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "csecrawler.settings")
import django
django.setup()

from notice_data.models import NoticeData


notice_base = 'https://computer.cnu.ac.kr/computer/notice'

notice_bachelor = '/bachelor.do'
notice_normal = '/notice.do'
notice_project = '/project.do'
notice_job = '/job.do'

notice_board = '?mode=list&&articleLimit=10&article.offset='

notice_selector = 'tr > td.b-td-left > div > a'

notice_dict = dict()


def fetch_cse_notices(notice_type):
    j = 0
    for i in range(3):
        offset = 10 * i
        req = requests.get(notice_base + notice_type + notice_board + str(offset))
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        notices = soup.select(notice_selector)

        for notice in notices:
            notice_post = notice.get('href')
            notice_link = notice_base + notice_type + notice_post

            req = requests.get(notice_link)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            notice_date = soup.find('td', {'class': 'b-no-right', 'colspan': '2'}).text
            notice_title = soup.find('td', {'class': 'b-title-box b-no-right'}).text
            notice_text = soup.find('pre', {'class': 'pre'}).text

            notice_dict[j] = {
                'link' : notice_link,
                'type' : notice_type,
                'date' : notice_date,
                'title': notice_title,
                'text': notice_text,
            }
            j += 1


def add_new_items(crawled_items):
    for key, val in crawled_items.items():
        if NoticeData.objects.filter(text=val['text']).exists() :
            print('[중복] :', val['title'])
        else :
            NoticeData(link=val['link'], type=val['type'], date=val['date'], title=val['title'], text=val['text']).save()
            print('[신규] :', val['title'])


if __name__=='__main__':
    #fetch_cse_notices(notice_bachelor)
    #fetch_cse_notices(notice_normal)
    fetch_cse_notices(notice_project)
    #fetch_cse_notices(notice_job)
    print('data fetched')
    add_new_items(notice_dict)
    print('data saved')