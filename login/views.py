from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
#from notice_data.models import NoticeData


def index(request):
	return render(request, 'login/index.html')
	#notices = NoticeData.objects.all()
	#context = {'notices':notices}
	#return render(request, 'notice/index.html', context)
