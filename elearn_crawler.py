# coding=utf-8
import requests
import json
import time
import copy
from django.utils import timezone
from bs4 import BeautifulSoup
from login.models import Profile
from elearn_data.models import ElearnData
from passlib.hash import cisco_type7
from time_handler import time_validation
from time_handler import convert_time
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures


cnuportal_login = 'https://portal.cnu.ac.kr/enview/user/login.face'
elearn_base = 'http://e-learning.cnu.ac.kr'
elearning_redirection = elearn_base + '/ksign/index.jsp'
elearn_notices_materials = elearn_base + '/lms/class/boardItem/doListView.dunet'
elearning_myLecture = elearn_base + '/lms/myLecture/doListView.dunet'
elearning_myClassroom = elearn_base + '/lms/class/classroom/doViewClassRoom_new.dunet'
classroom_course = elearn_base + '/lms/class/courseSchedule/doListView.dunet'
classroom_report = elearn_base + '/lms/class/report/stud/doListView.dunet'

LOGIN_INFO = dict()

s = requests.Session()


def fetch_and_save(profile):
    start_time = time.time()
    portal_login_web(profile.portal_id, profile.portal_pw)
    subject_dict = fetch_elearn()
    save_items(profile, subject_dict)
    print("[TIME] ELEARN FETCH AND SAVE TIME : %s sec" %(time.time() - start_time))
    return get_context(profile)


def fetch_and_update(profile):
    start_time = time.time()
    portal_login_web(profile.portal_id, profile.portal_pw)
    subject_dict = fetch_elearn()
    update_items(profile, subject_dict)
    print("[TIME] ELEARN FETCH AND UPDATE TIME : %s sec" %(time.time() - start_time))
    return get_context(profile)


def get_context(profile):
    start_time = time.time()
    elearns = ElearnData.objects.filter(userID=profile)
    if not elearns:
        elearns = None
        videosDetail = ['크롤링된 데이터가 없습니다. 포탈 비밀번호를 확인해주세요.']
        reportsDetail = ['크롤링된 데이터가 없습니다. 포탈 비밀번호를 확인해주세요.']

        context = {
            'profile': profile,
            'classes': elearns,
            'videosDetail': videosDetail,
            'reportsDetail': reportsDetail
        }
    else:
        videosDetail = []
        reportsDetail = []
        noticesDetail = []
        materialsDetail = []

        for i in range(len(elearns)):
            elearns[i].videos = json.loads(elearns[i].videos)
            elearns[i].reports = json.loads(elearns[i].reports)

        for data in elearns:
            videosDetailTemp = json.loads(data.videosDetail)
            for video in videosDetailTemp:
                data_list = list()
                data_list.append(video)
                data_list.append(videosDetailTemp.get(video))
                videosDetail.append(data_list)

            reportsDetailTemp = json.loads(data.reportsDetail)
            for report in reportsDetailTemp:
                data_list = list()
                data_list.append(report)
                data_list.append(reportsDetailTemp.get(report))
                reportsDetail.append(data_list)

            noticesTemp = json.loads(data.notices)
            for notice in noticesTemp:
                data_list = list()
                data_list.append(notice)
                data_list.append(noticesTemp.get(notice))
                noticesDetail.append(data_list)

            materialsTemp = json.loads(data.materials)
            for material in materialsTemp:
                data_list = list()
                data_list.append(material)
                data_list.append(materialsTemp.get(material))
                materialsDetail.append(data_list)

        context = {
            'profile': profile,
            'classes': elearns,
            'videosDetail': videosDetail,
            'reportsDetail': reportsDetail,
            'noticesDetail': noticesDetail,
            'materialsDetail': materialsDetail,
        }

    print("[TIME] GET_CONTEXT TIME : %s sec" %(time.time() - start_time))
    return context


def fetch_and_show():
    portal_login_terminal()
    subject_dict = fetch_elearn()
    dict_show(subject_dict)


def portal_login_web(id_portal, pw_portal):
    LOGIN_INFO['userId'] = id_portal
    LOGIN_INFO['password'] = cisco_type7.decode(pw_portal)


def portal_login_terminal():
    print('***Login portal.cnu.ac.kr***')
    id_portal = input('ID : ')
    pw_portal = input('PW : ')
    LOGIN_INFO['userId'] = id_portal
    LOGIN_INFO['password'] = pw_portal


def save_items(profile, data):
    for key, val in data.items():
        ElearnData(
            userID=profile,
            title=val['name'],
            percentage=val['percentage'],
            videos=val['videos'],
            reports=val['reports'],
            videosDetail=val['videosDetail'],
            reportsDetail=val['reportsDetail'],
            notices=val['notices'],
            materials=val['materials']
        ).save()
        print('Data', val['name'], 'saved!')
    profile.last_update = timezone.now()
    profile.save()


def update_items(profile, data):
    for key, val in data.items():
        if ElearnData.objects.filter(userID=profile, title=val['name']).exists():
            target = ElearnData.objects.get(userID=profile, title=val['name'])
            target.percentage = val['percentage']
            target.videos = val['videos']
            target.reports = val['reports']
            target.videosDetail = val['videosDetail']
            target.reportsDetail = val['reportsDetail']
            target.notices = val['notices']
            target.materials = val['materials']
            target.save()
            print('Data', val['name'], 'updated!')
    profile.last_update = timezone.now()
    profile.save()


def clear_items(profile):
    targets = ElearnData.objects.filter(userID=profile)
    for target in targets:
        target.delete()


def show_dict(dict):
    for key, value in dict.items():
        print('+++' * 10)
        print(value['name'], value['percentage'])
        print(value['videos'], value['reports'])


def fetch_elearn():
    class_info = dict()
    login = s.post(cnuportal_login, data=LOGIN_INFO)
    elearn = s.get(elearning_redirection, verify=False)
    myLecture = s.get(elearning_myLecture, verify=False)

    elearn_html = myLecture.text
    elearn_soup = BeautifulSoup(elearn_html, 'html.parser')
    subjects = elearn_soup.find_all('a', {'class': 'classin2'})
    subject_dict = dict()

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
        print(course_name)

        video_statistics = [0, 0, 0, 0, 0]
        videosDetail = dict()

        i = 0
        for status in statistics:
            if status.text.find('~ 20') != -1 and status.text.find('학습기간') == -1:
                dues.append(status.text[19:].replace('\t', '').replace('\n', '').replace('\r', '').rstrip())
                i += 1
            if status.text.find('출석완료') != -1:
                video_statistics[0] += 1
            if status.text.find('진행중') != -1:
                video_statistics[1] += 1
                videosDetail[course_name + names[i - 1].text[0:50].strip().replace('\n', '').replace('\t', '')] = convert_time(dues[-1], '%Y.%m.%d %H:%M')
            if status.text.find('미진행') != -1:
                video_statistics[2] += 1
                if time_validation(dues[-1], '%Y.%m.%d %H:%M', 0):
                    videosDetail[course_name + names[i - 1].text[0:50].strip().replace('\n', '').replace('\t', '')] = convert_time(dues[-1], '%Y.%m.%d %H:%M')
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
        reportsDetail = dict()

        i = 0
        for status in statistics:
            if status.text.find('미제출') != -1:
                report_statistics[1] += 1
                endDateTime = dues[i].text[26:].replace('\t', '').replace('\n', '').replace('\r', '')
                if time_validation(endDateTime, "%y/%m/%d %H:%M", 0):
                    reportsDetail[course_name + names[i].text.strip().replace('\n', '').replace('\t', '')] = convert_time(endDateTime, "%y/%m/%d %H:%M")
                i += 1
            elif status.text.find('제출') != -1:
                report_statistics[0] += 1
                i += 1
                
        #성철이 형이 짠 부분   
        NOTICE_INFO = {
            'mnid' : '201008945595',
            'board_no' : '7'
            #과목 공지
        }
        REFER_INFO = {
            'mnid' : '20100863099',
            'board_no' : '6'
            #자료실
        }

        notices = dict()
        materials = dict()

        board_refer = s.post(elearn_notices_materials, data=REFER_INFO)
        board_notice = s.post(elearn_notices_materials, data=NOTICE_INFO)
        board_refer_html = BeautifulSoup(board_refer.text, 'html.parser')
        board_notice_html = BeautifulSoup(board_notice.text, 'html.parser')

        notice = board_notice_html.find('tbody')
                
        arr_size = len(notice.find_all('td'))
        for n in range(int(arr_size/6)):
                    
            notice_title = course_name + notice.find_all('td')[n*6 + 1].text.replace('\t','').replace('\n','').replace('\r','').strip()
            notice_date = notice.find_all('td')[n*6 + 4].text
        
            if time_validation(notice_date, "%Y.%m.%d", 14):
                notices[notice_title] = convert_time(notice_date, '%Y.%m.%d', dateonly=True)

        material = board_refer_html.find('tbody')
                
        arr_size = len(material.find_all('td'))
        for n in range(int(arr_size/6)):
            material_title = course_name + material.find_all('td')[n*6 + 1].text.replace('\t','').replace('\n','').replace('\r','').strip()
            material_date = material.find_all('td')[n*6 + 4].text
            if time_validation(material_date, "%Y.%m.%d", 14):
                materials[material_title] = convert_time(material_date, '%Y.%m.%d', dateonly=True)

        # 성철이 형이 짠 부분
        subject_dict[key]['name'] = course_name
        subject_dict[key]['percentage'] = class_percentage
        subject_dict[key]['videos'] = json.dumps(video_statistics)
        subject_dict[key]['reports'] = json.dumps(report_statistics)
        subject_dict[key]['videosDetail'] = json.dumps(videosDetail, ensure_ascii=False, indent="\t")
        subject_dict[key]['reportsDetail'] = json.dumps(reportsDetail, ensure_ascii=False, indent="\t")
        subject_dict[key]['notices'] = json.dumps(notices, ensure_ascii=False, indent="\t")
        subject_dict[key]['materials'] = json.dumps(materials, ensure_ascii=False, indent="\t")

    print(subject_dict)
        
    return subject_dict


def main():
    fetch_and_show()


if __name__ == '__main__':
    main()
