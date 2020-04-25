from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
#from notice_data.models import NoticeData


def signin(request):
	return render(request, 'login/signin.html')


def login(request):
	return render(request, 'login/login.html')
	#notices = NoticeData.objects.all()
	#context = {'notices':notices}
	#return render(request, 'notice/index.html', context)
