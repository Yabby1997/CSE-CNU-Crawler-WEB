# coding=utf-8
import requests
import json
from bs4 import BeautifulSoup
from login.models import Profile
from elearn_data.models import ElearnData
from django.utils import timezone
from datetime import datetime
import pytz

cnuportal_login = 'https://portal.cnu.ac.kr/enview/user/login.face'
elearn_base = 'http://e-learn.cnu.ac.kr'
elearning_redirection = elearn_base + '/ksign/index.jsp'
elearning_myLecture = elearn_base + '/lms/myLecture/doListView.dunet'
elearning_myClassroom = elearn_base + '/lms/class/classroom/doViewClassRoom_new.dunet'
classroom_course = elearn_base + '/lms/class/courseSchedule/doListView.dunet'
classroom_report = elearn_base + '/lms/class/report/stud/doListView.dunet'

LOGIN_INFO = dict()
subject_dict = dict()

def fetch_and_save(profile):
    portal_login_web(profile.portal_id, profile.portal_pw)
    fetch_elearn()
    add_new_items(profile, subject_dict)
    return get_context(profile)


def get_context(profile):
    elearns = ElearnData.objects.filter(userID=profile)
    videos2watch = []
    reports2do = []

    for data in elearns:
        videos = json.loads(data.videos2watch)
        for video in videos:
            videos2watch.append(video)

        reports = json.loads(data.reports2do)
        for report in reports:
            reports2do.append(report)

    context = {
        'profile': profile,
        'classes': elearns,
        'videos': videos2watch,
        'reports': reports2do,
    }
    return context


def fetch_and_show():
    portal_login_terminal()
    fetch_elearn()
    dict_show(subject_dict)


def portal_login_web(id_portal, pw_portal):
    LOGIN_INFO['userId'] = id_portal
    LOGIN_INFO['password'] = pw_portal


def portal_login_terminal():
    print('***Login portal.cnu.ac.kr***')
    id_portal = input('ID : ')
    pw_portal = input('PW : ')
    LOGIN_INFO['userId'] = id_portal
    LOGIN_INFO['password'] = pw_portal


def add_new_items(profile, data):
    for key, val in data.items():
        if ElearnData.objects.filter(userID=profile, title=val['name']).exists():
            target = ElearnData.objects.get(userID=profile, title=val['name'])
            target.percentage = val['percentage']
            target.video0 = val['videos'][0]
            target.video1 = val['videos'][1]
            target.video2 = val['videos'][2]
            target.video3 = val['videos'][3]
            target.video4 = val['videos'][4]
            target.report0 = val['reports'][0]
            target.report1 = val['reports'][1]
            target.videos2watch = val['videos2watch']
            target.reports2do = val['reports2do']
            target.save()
            print('Data', val['name'], 'updated!')
        else:
            ElearnData(
                userID=profile,
                title=val['name'],
                percentage=val['percentage'],
                video0=val['videos'][0],
                video1=val['videos'][1],
                video2=val['videos'][2],
                video3=val['videos'][3],
                video4=val['videos'][4],
                report0=val['reports'][0],
                report1=val['reports'][1],
                videos2watch=val['videos2watch'],
                reports2do=val['reports2do'],
            ).save()
            print('Data', val['name'], 'saved!')
    profile.last_update = timezone.now()
    profile.save()


def show_dict(dict):
    for key, value in dict.items():
        print('+++' * 10)
        print(value['name'], value['percentage'])
        print(value['videos'], value['reports'])


def convert_time(endDateTime, mask):
    endDateTime = datetime.strptime(endDateTime, mask)
    endDateTime = endDateTime.replace(tzinfo=pytz.timezone('Asia/Seoul'))
    now = datetime.now(pytz.timezone('Asia/Seoul'))
    delta = endDateTime - now
    days = str(delta.days)
    hours = str(delta.seconds // 3600)
    return days, hours


def fetch_elearn():
    with requests.Session() as s:
        login = s.post(cnuportal_login, data=LOGIN_INFO)
        elearn = s.get(elearning_redirection, verify=False)
        myLecture = s.get(elearning_myLecture, verify=False)

        elearn_html = myLecture.text
        elearn_soup = BeautifulSoup(elearn_html, 'html.parser')
        subjects = elearn_soup.find_all('a', {'class': 'classin2'})

        i = 0
        for subject in subjects:
            class_id = subject.get('course_id')
            class_no = subject.get('class_no')

            subject_dict[i] = {
                'id': class_id,
                'no': class_no,
            }
            i += 1

        for key, value in subject_dict.items():
            CLASS_INFO = {
                'mnid': '201008840728',
                'course_id': value['id'],
                'class_no': value['no']
            }
            classroom = s.post(elearning_myClassroom, data=CLASS_INFO)
            classroom_html = classroom.text
            classroom_soup = BeautifulSoup(classroom_html, 'html.parser')
            class_percentage = classroom_soup.find('span', {'class': "num"}).text.replace('(', '').replace(')', '')

            course = s.get(classroom_course, verify=False)
            course_html = course.text
            course_soup = BeautifulSoup(course_html, 'html.parser')
            course_name = course_soup.find('p', {'class': "list_tit"}).text.replace('과목명 | ', '')
            statistics = course_soup.find_all('td')
            names = course_soup.find_all('td', {'style': 'text-align:left;padding-left:10px;'})
            dues = []

            video_statistics = [0, 0, 0, 0, 0]
            videos2watch = []

            for status in statistics:
                if status.text.find('~ 20') != -1 and status.text.find('학습기간') == -1:
                    dues.append(status.text[19:].replace('\t', '').replace('\n', '').replace('\r', '').rstrip())
                if status.text.find('출석완료') != -1:
                    video_statistics[0] += 1
                if status.text.find('진행중') != -1:
                    video_statistics[1] += 1
                    days, hours = convert_time(dues[-1], '%Y.%m.%d %H:%M')
                    videos2watch.append(course_name + names[-1].text[0:50].strip().replace('\n', '').replace('\t', '') + '   출석까지 '+ days + '일 ' + hours + '시간 남음')
                if status.text.find('미진행') != -1:
                    video_statistics[2] += 1
                    days, hours = convert_time(dues[-1], '%Y.%m.%d %H:%M')
                    videos2watch.append(course_name + names[-1].text[0:50].strip().replace('\n', '').replace('\t', '') + '   출석까지 '+ days + '일 ' + hours + '시간 남음')
                if status.text.find('학습시작전') != -1:
                    video_statistics[2] -= 1
                    video_statistics[3] += 1
                if status.text.find('미수강') != -1:
                    video_statistics[4] += 1

            report = s.get(classroom_report, verify=False)
            report_html = report.text
            report_soup = BeautifulSoup(report_html, 'html.parser')
            statistics = report_soup.find_all('td', {'class': 'ta_c txt1'})
            names = report_soup.select('table.datatable.mg_t10.fs_s > tbody > tr > td.ta_l > strong > a')
            dues = report_soup.select('table.datatable.mg_t10.fs_s > tbody > tr > td > a')
            report_statistics = [0, 0]
            reports2do = []
            
            i = 0
            for status in statistics:
                if status.text.find('제출') != -1:
                    report_statistics[0] += 1
                    i += 1
                if status.text.find('미제출') != -1:
                    report_statistics[1] += 1
                    endDateTime = dues[i - 1].text[26:].replace('\t', '').replace('\n', '').replace('\r', '')
                    days, hours = convert_time(endDateTime, "%y/%m/%d %H:%M")
                    reports2do.append(course_name + names[i - 1].text.strip().replace('\n', '').replace('\t', '') + '   제출까지 '+ days + '일 ' + hours + '시간 남음')
                    i += 1

            subject_dict[key]['name'] = course_name
            subject_dict[key]['percentage'] = class_percentage
            subject_dict[key]['videos'] = video_statistics
            subject_dict[key]['reports'] = report_statistics
            subject_dict[key]['videos2watch'] = json.dumps(videos2watch, ensure_ascii=False, indent="\t")
            subject_dict[key]['reports2do'] = json.dumps(reports2do, ensure_ascii=False, indent="\t")


def main():
    fetch_and_show()


if __name__ == '__main__':
    main()
