from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile


def signup(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		confirm = request.POST['pw_confirm']
		id_portal = request.POST['id_portal']
		pw_portal = request.POST['pw_portal']

		if not (username and password and confirm and id_portal and pw_portal):
			return render(request, 'login/signup.html', {'error' : 'username or password is incorrect'})
		else:
			if password == confirm:
				user = User.objects.create_user(username=username, password=password)
				Profile(user=user, portal_id=id_portal, portal_pw=pw_portal).save()
				auth.login(request, user)
				return redirect('elearn')
	return render(request, 'login/signup.html')


def login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		if not (username and password):
			return render(request, 'login/login.html', {'error' : 'username or password is incorrect'})
		else:
			user = auth.authenticate(request, username=username, password=password)
			if user is not None:
				auth.login(request, user)
				return redirect('elearn')
			else:
				return render(request, 'login/login.html', {'error' : 'username or password is incorrect'})
	else:
		return render(request, 'login/login.html')

