from django.shortcuts import render, redirect
from .models import User, Alert
from random import randint
from .email_script import *
import datetime
import re
import bcrypt

email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
strong_password_pattern = re.compile(
	r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
)

def index(request):
	return render(request, 'index.html')

def signup(request):
	return render(request, 'signup.html')

def signin(request):
	return render(request, 'signin.html')

def signup_submit(request):
	email_in = request.POST.get('email')
	pswd1_in = request.POST.get('pswd1')
	pswd2_in = request.POST.get('pswd2')
	msg = ""
	st = ""
	if email_pattern.match(email_in) is None:
		st = 'message-box error'
		msg = 'Email pattern incorrect :('
	elif pswd1_in != pswd2_in:
		st = 'message-box error'
		msg = 'Passwords do not match :('
	elif strong_password_pattern.match(pswd1_in) is None:
		st = 'message-box warning'
		msg = 'Password weak :('
	else:
		request.session['email'] = email_in
		request.session['pswd'] = pswd1_in
		otp = randint(100000, 999999)
		otp = str(otp)
		print(otp)
		request.session['otp'] = otp
		send_email(email_in, "Email Verification", "Your OTP is: " + otp)
		return render(request, 'otp_check.html')
	return render(request, 'resp.html', {'st': st, 'msg': msg})

def otp_check(request):
	otp = request.POST.get('otp')
	copy = User.objects.filter(email = request.session['email'])
	if copy:
		st = 'message-box error'
		msg = 'Email already used :('
	elif otp != request.session['otp']:
		st = 'message-box error'
		msg = 'OTP incorrect :('
	else:
		salt = bcrypt.gensalt()
		pswd = bcrypt.hashpw(request.session['pswd'].encode('utf-8'), salt)
		user = User(email = request.session['email'], pswd_hash = pswd)
		user.save()
		return redirect('signin')
	return render(request, 'resp.html', {'st': st, 'msg': msg})

def signin_submit(request):
	email_in = request.POST.get('email')
	pswd_in = request.POST.get('pswd')
	pswd_in = pswd_in.encode('utf-8')
	st = ''
	msg = ''
	user = User.objects.filter(email = email_in)
	if user:
		user = User.objects.get(email = email_in)
	if user:
		if bcrypt.checkpw(pswd_in, user.pswd_hash):
			request.session['user'] = email_in
			request.session['alert'] = None
			return redirect('user')
		else:
			st = 'message-box error'
			msg = 'Password incorrect :('
	else:
		st = 'message-box error'
		msg = 'User does not exist! :('
	return render(request, 'resp.html', {'st': st, 'msg': msg})

def user_serve(request):
	user = User.objects.get(email = request.session['user'])
	alerts = Alert.objects.filter(user_id = user.id)
	return render(request, 'user.html', {'user': request.session['user'], 'alerts': alerts})

def user_delete(request):
	user = User.objects.filter(email = request.session['user'])
	user.delete()
	return redirect('index')

def alert(request):
	request.session['alert'] = None
	return render(request, 'alert.html', {'sp': '', 'f': ''})

def alert_create(request):
	t_in = request.POST.get('topic')
	sp_in = request.POST.get('search_phrase')
	f_in = request.POST.get('freq')
	f_in = int(f_in)
	if request.session['alert'] is None:
		u = User.objects.get(email = request.session['user'])
		l = datetime.date.today()
		n = l + datetime.timedelta(days = f_in)
		alert = Alert(topic = t_in, search_phrase = sp_in, freq = f_in, last_mail = l, next_mail = n, user = u)
		alert.save()
	else:
		alert = Alert.objects.get(id = request.session['alert'])
		alert.topic = t_in
		alert.search_phrase = sp_in
		alert.freq = f_in
		alert.save()
		request.session['alert'] = None
	return redirect('user')

def alert_delete(request):
	alert = Alert.objects.get(id = request.session['alert'])
	alert.delete()
	return redirect('user')

def alert_get(request, alert_id):
	request.session['alert'] = alert_id
	alert = Alert.objects.get(id = alert_id)
	return render(request, 'alert.html', {'sp': alert.search_phrase, 'f': str(alert.freq)})