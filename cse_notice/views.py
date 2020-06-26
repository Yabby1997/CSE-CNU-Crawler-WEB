from django.shortcuts import render, redirect
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

	return render(request, 'notice/notice.html', context)


def elearn(request):
	if request.user.is_authenticated :
		profile = Profile.objects.get(user=request.user)
		context = {'user': request.user, 'elearn': ec.get_context(profile)}
		if request.method == "POST":
			context['elearn'] = ec.fetch_and_update(profile)
		return render(request, 'notice/elearn.html', context)

	else:
		return redirect('login')