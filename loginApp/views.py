from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):
	return render(request, 'login.html')


def register(request):
	print(request.POST)
	print('************')
	errorValidator = User.objects.regValidator(request.POST)

	if len(errorValidator) > 0:
		for key, value in errorValidator.items():
			messages.error(request, value)
			print('******', errorValidator)
		return redirect('/')
	password = request.POST['pword']
	pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
	print(pw_hash)
	newuser = User.objects.create(firstName = request.POST['fname'], lastName = request.POST['lname'],
	Email = request.POST['email'], Password = pw_hash, birthday = request.POST['bday'])
	
	request.session['loggedInUserId'] = newuser.id
	
	return redirect('/success')



def login(request):
	print(request.POST)
	print('*********')
	errorValidator = User.objects.loginValidator(request.POST)
	if len(errorValidator) > 0:
		for key, value in errorValidator.items():
			messages.error(request, value)
			print('******', errorValidator)
		return redirect('/')
	user = User.objects.filter(Email=request.POST['emaillogin'])	
	if user:
		logged_user = user[0]

		if bcrypt.checkpw(request.POST['pwlogin'].encode(), logged_user.Password.encode()):
			request.session['loggedInUserId'] = logged_user.id

		return redirect('/success')
	return redirect("/")

def success(request):
	if 'loggedInUserId' not in request.session:
		messages.error(request, 'You must be logged in to view the main page')
		return redirect('/')
	context = {
		"loggedInUser": User.objects.get(id=request.session['loggedInUserId'])
	}
	return render(request, 'success.html', context)


def logout(request):
	request.session.clear()
	return redirect('/')