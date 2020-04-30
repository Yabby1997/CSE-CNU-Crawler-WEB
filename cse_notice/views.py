from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from notice_data.models import NoticeData
from elearn_data.models import ElearnData
from login.models import Profile
import elearn_crawler as ec


def notice(request):
	notices = NoticeData.objects.all()
	context = {'notices': notices}
	return render(request, 'notice/notice.html', context)


def elearn(request):
	profile = Profile.objects.get(user=request.user)
	context = ec.get_context(profile)
	if request.method == "POST":
		context = ec.fetch_and_update(profile)
	return render(request, 'notice/elearn.html', context)