from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from notice_data.models import NoticeData
from elearn_data.models import ElearnData
from login.models import Profile
import elearn_crawler as ec
import json


def notice(request):
	notices = NoticeData.objects.all()
	context = {'notices': notices}
	return render(request, 'notice/notice.html', context)


def elearn(request):
	profile = Profile.objects.get(user=request.user)
	if request.method == "POST":
		ec.fetch_and_save(profile)
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
		return render(request, 'notice/elearn.html', context)
	return render(request, 'notice/elearn.html')