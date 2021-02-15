from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from notice_data.models import NoticeData
from elearn_data.models import ElearnData
from login.models import Profile
import elearn_crawler as ec
import cse_crawler as cc
from passlib.hash import cisco_type7
from django.template import RequestContext


def bad_request(request, exception) :
	return render(request, 'notice/400.html', status=400)


def permission_denied(request, exception) :
	return render(request, 'notice/403.html', status=403)


def page_not_found(request, exception) :
	return render(request, 'notice/404.html', status=404)


def server_error(request) :
	return render(request, 'notice/500.html', status=500)


def csenotice(request):
	if request.method == "POST":
		cc.fetch_and_save()
	context = {'notices': NoticeData.objects.all()}
	return render(request, 'notice/csenotices.html', context)


def video(request):
	if request.user.is_authenticated :
		profile = Profile.objects.get(user=request.user)
		context = {'user': request.user, 'elearn': ec.get_context(profile)}
		if request.method == "POST":
			context['elearn'] = ec.fetch_and_update(profile)
		return render(request, 'notice/videos.html', context)

	else:
		return redirect('login')


def report(request):
	if request.user.is_authenticated :
		profile = Profile.objects.get(user=request.user)
		context = {'user': request.user, 'elearn': ec.get_context(profile)}
		if request.method == "POST":
			context['elearn'] = ec.fetch_and_update(profile)
		return render(request, 'notice/report.html', context)

	else:
		return redirect('login')


def notice(request):
	if request.user.is_authenticated :
		profile = Profile.objects.get(user=request.user)
		context = {'user': request.user, 'elearn': ec.get_context(profile)}
		if request.method == "POST":
			context['elearn'] = ec.fetch_and_update(profile)
		return render(request, 'notice/notice.html', context)

	else:
		return redirect('login')


def material(request):
	if request.user.is_authenticated :
		profile = Profile.objects.get(user=request.user)
		context = {'user': request.user, 'elearn': ec.get_context(profile)}
		if request.method == "POST":
			context['elearn'] = ec.fetch_and_update(profile)
		return render(request, 'notice/material.html', context)

	else:
		return redirect('login')


def mainpage(request):
	if request.user.is_authenticated :
		profile = Profile.objects.get(user=request.user)
		context = {'user': request.user, 'elearn': ec.get_context(profile)}
		if request.method == "POST":
			context['elearn'] = ec.fetch_and_update(profile)
		return render(request, 'notice/main.html', context)

	else:
		return redirect('login')


#link test
