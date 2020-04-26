from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile


def signup(request):
	if request.method == "POST":
		if request.POST["password"] == request.POST["pw_confirm"]:
			user = User.objects.create_user(
				username=request.POST["username"],
				password=request.POST["password"]
				)
			
			profile = Profile(
				user=user,
				portal_id=request.POST["id_portal"],
				portal_pw=request.POST["pw_portal"]
				)
			profile.save()
			return redirect('login')
	return render(request, 'login/signup.html')


def login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(request, username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('notice')
		else:
			return render(request, 'login/login.html', {'error' : 'username or password is incorrect'})
	else:
		return render(request, 'login/login.html')

