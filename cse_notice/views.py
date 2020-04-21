import json
from json2html import *
from django.views import View

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

#from .models import Candidate

import requests
from bs4 import BeautifulSoup
import os

notice_base = 'https://computer.cnu.ac.kr/computer/notice/project.do'
notice_url = 'https://computer.cnu.ac.kr/computer/notice/project.do?mode=list&&articleLimit=10&article.offset='
cnuportal_login = 'https://portal.cnu.ac.kr/enview/user/login.face'
elearning_redirection = 'http://e-learn.cnu.ac.kr/ksign/index.jsp'
elearning_myLecture = 'http://e-learn.cnu.ac.kr/lms/myLecture/doListView.dunet'
elearning_myClassroom = 'http://e-learn.cnu.ac.kr/lms/class/classroom/doViewClassRoom_new.dunet'
classroom_course = 'http://e-learn.cnu.ac.kr/lms/class/courseSchedule/doListView.dunet'
classroom_report = 'http://e-learn.cnu.ac.kr/lms/class/report/stud/doListView.dunet'

notice_dict = dict()
subject_dict = dict()
subject_percentage = list()


def index(request):
	'''
	notice_selector = 'tr > td.b-td-left > div > a'

	data = ''

	j = 0
	for i in range(1):
		offset = 10 * i
		req = requests.get(notice_url + str(offset))
		html = req.text
		soup = BeautifulSoup(html, 'html.parser')
		notices = soup.select(notice_selector)

		for notice in notices:
			notice_append = notice.get('href')
			notice_dict[j] = {
				'title' : notice.get('title'),
				'text' : ""
			}
			req = requests.get(notice_base + notice_append)
			html = req.text
			soup = BeautifulSoup(html, 'html.parser')
			text = soup.find('pre', {'class' : 'pre'}).text
			notice_dict[j]['text'] = text
			j += 1

	notice_json = json.dumps(notice_dict)
	infoFromJson = json.loads(notice_json)
	data += json2html.convert(json=infoFromJson)

	LOGIN_INFO = {
		'userId': '201602022',
		'password': 'qwe123!@#'
	}

	with requests.Session() as s:
		login = s.post(cnuportal_login, data=LOGIN_INFO)
		elearn = s.get(elearning_redirection, verify=False)
		myLecture = s.get(elearning_myLecture, verify=False)

		elearn_html = myLecture.text
		elearn_soup = BeautifulSoup(elearn_html, 'html.parser')
		subjects = elearn_soup.find_all('a', {'class': 'classin2'})

		i = 0
		for subject in subjects:
			subject_dict[i] = {
				'id': subject.get('course_id'),
				'no': subject.get('class_no'),
				'name': "",
				'percentage': "",
				'finished': "",
				'proceeding': "",
				'unseen': "",
				'notyet': "",
				'repo_fin': "",
				'repo_notfin': ""
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
			class_percentage = classroom_soup.find('span', {'class': "num"}).text
			subject_percentage.append(class_percentage)

			course = s.get(classroom_course, verify=False)
			course_html = course.text
			course_soup = BeautifulSoup(course_html, 'html.parser')
			course_name = course_soup.find('p', {'class': "list_tit"}).text
			subject_dict[key]['name'] = course_name.replace('과목명 | ', '')
			subject_dict[key]['percentage'] = subject_percentage[key].replace('(', '').replace(')', '')

			lectures = course_soup.find_all('td')

			finished = 0
			proceeding = 0
			unseen = 0
			notyet = 0

			for lecture in lectures:
				if lecture.text.find('출석완료') != -1:
					finished += 1
				if lecture.text.find('진행중') != -1:
					proceeding += 1
				if lecture.text.find('미진행') != -1:
					unseen += 1
				if lecture.text.find('학습시작전') != -1:
					unseen -= 1
					notyet += 1

			subject_dict[key]['finished'] = finished
			subject_dict[key]['proceeding'] = proceeding
			subject_dict[key]['unseen'] = unseen
			subject_dict[key]['notyet'] = notyet

			report = s.get(classroom_report, verify=False)
			report_html = report.text
			report_soup = BeautifulSoup(report_html, 'html.parser')

			reports = report_soup.find_all('td')

			repo_fin = 0
			repo_notfin = 0

			for report in reports:
				if report.text.find('미제출') != -1:
					repo_notfin += 1
				if report.text.find('제출') != -1:
					repo_fin += 1

			subject_dict[key]['repo_fin'] = repo_fin
			subject_dict[key]['repo_notfin'] = repo_notfin

		subject_json = json.dumps(subject_dict)
		infoFromJson = json.loads(subject_json)
		data += json2html.convert(json=infoFromJson)
	'''
	#return HttpResponse(data)
	return render(request, 'notice/index.html')