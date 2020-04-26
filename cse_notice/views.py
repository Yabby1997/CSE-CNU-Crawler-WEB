from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from notice_data.models import NoticeData


def notice(request):
	notices = NoticeData.objects.all()
	context = {'notices':notices}
	return render(request, 'notice/notice.html', context)


def elearn(request):
	return render(request, 'notice/elearn.html')
