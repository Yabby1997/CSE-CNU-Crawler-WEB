# coding=utf-8
import requests
from bs4 import BeautifulSoup

cnuportal_login = 'https://portal.cnu.ac.kr/enview/user/login.face'
elearn_base = 'http://e-learn.cnu.ac.kr'
elearning_redirection = elearn_base + '/ksign/index.jsp'
elearning_myLecture = elearn_base + '/lms/myLecture/doListView.dunet'
elearning_myClassroom = elearn_base + '/lms/class/classroom/doViewClassRoom_new.dunet'
classroom_course = elearn_base + '/lms/class/courseSchedule/doListView.dunet'
classroom_report = elearn_base + '/lms/class/report/stud/doListView.dunet'

subject_dict = dict()


def dict_show(dict):
	for key, value in dict.items():
		print('+++' * 10)
		print(value['name'], value['percentage'])
		print(value['videos'], value['reports'])


def main():
	with requests.Session() as s:
		print('***Login portal.cnu.ac.kr***')
		id_portal = input('ID : ')
		pw_portal = input('PW : ')

		LOGIN_INFO = {
			'userId': id_portal,
			'password': pw_portal
		}

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
			statistics = course_soup.find_all('td', {'class': 'ag_c pd_ln'})

			video_statistics = [0, 0, 0, 0, 0]

			for status in statistics:
				if status.text.find('출석완료') != -1:
					video_statistics[0] += 1
				if status.text.find('진행중') != -1:
					video_statistics[1] += 1
				if status.text.find('미진행') != -1:
					video_statistics[2] += 1
				if status.text.find('학습시작전') != -1:
					video_statistics[2] -= 1
					video_statistics[3] += 1
				if status.text.find('미수강') != -1:
					video_statistics[4] += 1


			report = s.get(classroom_report, verify=False)
			report_html = report.text
			report_soup = BeautifulSoup(report_html, 'html.parser')
			statistics = report_soup.find_all('td', {'class': 'ta_c txt1'})

			report_statistics = [0, 0]

			for status in statistics:
				if status.text.find('제출') != -1:
					report_statistics[0] += 1
				if status.text.find('미제출') != -1:
					report_statistics[1] += 1

			subject_dict[key]['name'] = course_name
			subject_dict[key]['percentage'] = class_percentage
			subject_dict[key]['videos'] = video_statistics
			subject_dict[key]['reports'] = report_statistics

		dict_show(subject_dict)

if __name__ == '__main__':
	main()
