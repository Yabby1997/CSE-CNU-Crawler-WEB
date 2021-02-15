import django
import time
import requests
import re
import os
from django.http import HttpResponse, JsonResponse
from bs4 import BeautifulSoup
from notice_data.models import NoticeData
from time_handler import time_validation
import concurrent.futures   
from concurrent.futures import ThreadPoolExecutor


os.environ.setdefault('DJANGO_SETTINGS_MODULE', "csecrawler.settings")
django.setup()

cse_base = 'https://computer.cnu.ac.kr/computer/notice'

bachelor_notice = '/bachelor.do'
normal_notice = '/notice.do'
project_notice = '/project.do'
job_notice = '/job.do'
notice_board = '?mode=list&&articleLimit=10&article.offset='

notice_selector = 'tr > td.b-td-left > div > a'

def fetch_cse_notices(category):
    notice_dict = dict()
    notice_index = 0

    for i in range(3):
        offset = 10 * i
        req = requests.get(cse_base + category + notice_board + str(offset))
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        notices = soup.select(notice_selector)

        if not notices:
            break

        for notice in notices:
            notice_post = notice.get('href')
            notice_link = cse_base + category + notice_post

            req = requests.get(notice_link)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            notice_date = soup.find('td', {'class': 'b-no-right', 'colspan': '2'}).text
            notice_title = soup.find('td', {'class': 'b-title-box b-no-right'}).text
            notice_type = soup.find('h3').text
            notice_number = re.findall("\d+", notice_post)[0]

            if notice_type == '학사공지':
                notice_number += '00'
            elif notice_type == '일반소식':
                notice_number += '01'
            elif notice_type == '사업단소식':
                notice_number += '10'
            else:
                notice_number += '11'

            if time_validation(notice_date, '%Y.%m.%d', 30):
                notice_dict[notice_index] = {
                    'link': notice_link,
                    'type': notice_type,
                    'date': notice_date,
                    'title': notice_title,
                    'number': notice_number,
                }
                notice_index += 1
    
    return add_new_items(notice_dict)


def add_new_items(crawled_data):
    new = 0
    for key, val in crawled_data.items():
        if NoticeData.objects.filter(number=val['number']).exists():
            print('[중복] :', val['title'])
        else:
            NoticeData(link=val['link'], type=val['type'], date=val['date'], title=val['title'],
                       number=val['number']).save()
            print('[신규] :', val['title'])
            new += 1
    return new


def fetch_and_save():
    start_time = time.time()

    thread_list = []
    new_count = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        for each in [normal_notice, bachelor_notice, project_notice]:
            thread_list.append(executor.submit(fetch_cse_notices, each))

        for future in concurrent.futures.as_completed(thread_list):
            new_count += future.result()

    print(new_count, 'new notice data successfully saved!')
    print("[TIME] CSE FETCH AND SAVE TIME : %s sec" %(time.time() - start_time))


if __name__ == '__main__':
    fetch_and_save()
