from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from notice_data.models import NoticeData
from elearn_data.models import ElearnData
from login.models import Profile
import elearn_crawler as ec
from passlib.hash import cisco_type7


def notice(request):
	notices = NoticeData.objects.all()
	context = {'notices': notices}

	profiles = Profile.objects.all()
	for profile in profiles.iterator():
		profile.portal_pw = cisco_type7.hash(profile.portal_pw)
		profile.save()
		print(profile.portal_id, 'done!')

	return render(request, 'notice/notice.html', context)


def elearn(request):
	profile = Profile.objects.get(user=request.user)
	context = {'user': request.user, 'elearn': ec.get_context(profile)}
	if request.method == "POST":
		context['elearn'] = ec.fetch_and_update(profile)
	return render(request, 'notice/elearn.html', context)