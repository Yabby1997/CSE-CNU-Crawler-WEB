from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import Profile


def signup(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		confirm = request.POST['pw_confirm']
		id_portal = request.POST['id_portal']
		pw_portal = request.POST['pw_portal']

		if not (username and password and confirm and id_portal and pw_portal):
			return render(request, 'login/signup.html')
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
			return render(request, 'login/login.html')
		else:
			user = auth.authenticate(request, username=username, password=password)
			if user is not None:
				auth.login(request, user)
				return redirect('elearn')
			else:
				return render(request, 'login/login.html')
	else:
		return render(request, 'login/login.html')


def setting(request):
	if request.method == "POST":
		password_old = request.POST['password_old']
		password = request.POST['password']
		confirm = request.POST['pw_confirm']
		pw_portal = request.POST['pw_portal']

		if not (password_old and password and confirm):
			return render(request, 'login/setting.html')
		else:
			user = request.user
			profile = Profile.objects.get(user=request.user)
			if check_password(password_old, user.password):
				if password == confirm:
					user.set_password(password)
					user.save()
					profile.portal_pw = pw_portal
					profile.save()
					auth.login(request, user)
				else:
					return render(request, 'login/setting.html')
			return redirect('elearn')
	return render(request, 'login/setting.html')