from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from validate_email import validate_email

ACCT_SIGNUP='accounts/signup.html'
def signup(request):
	if request.method == 'POST':
		#user wants to sign up
		if request.POST['password'] == request.POST['confirmpassword']:
			if not validate_email(request.POST['email']):
				return render(request,ACCT_SIGNUP,{"error": "Please enter a valid email"})
			try:
				user = User.objects.get(username=request.POST['username'])
				return render(request,ACCT_SIGNUP,{"error": "Username has already been taken"})
			except User.DoesNotExist:
				user = User.objects.create_user(
					username=request.POST['username'],
					password=request.POST["password"],
					first_name=request.POST['firstname'],
					last_name=request.POST['lastname'],
					email=request.POST['email'])
				auth.login(request,user)
				return redirect('home')

		else:
			return render(request,ACCT_SIGNUP,{"error": "Passwords do not match."})
	else:
		return render(request, ACCT_SIGNUP)

def signin(request):
	if request.method == "POST":
		
		user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			auth.login(request,user)	
			return redirect('home')
		else:
			return render(request,"accounts/signin.html",{"error": "You have entered an invalid username or password"})
	else:
		return render(request,'accounts/signin.html')

def signout(request):
	if request.method == "POST":
		auth.logout(request)
		return redirect('home')