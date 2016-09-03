from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db.models import F, Count

import markdown
import bleach

def compileMd(text): return bleach.clean(markdown.markdown(text), tags=['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'p', 'strong', 'table', 'td', 'tr', 'tt', 'ul'])

from .models import Message
from .forms import ReplyForm

# Create your views here.

def index(request):
	return redirect('/messages/1/')

def detail(request, msg_id):
	try:
		msg = Message.objects.get(pk=msg_id)
	except Message.DoesNotExist:
		raise Http404("Message does not exist")
	replies = Message.objects.filter(parent_message=msg).annotate(num_replies=Count('replies')).order_by('-pub_date').order_by('-num_replies')
	form = ReplyForm()
	return render(request, 'responda_messages/detail.html', {
		'message': msg,
		'msg_text': compileMd(msg.message_text),
		'replies': replies,
		'form': form
		})

@login_required
def reply(request, msg_id):
	try:
		parent_msg = Message.objects.get(pk=msg_id)
	except Message.DoesNotExist:
		raise Http404("Message does not exist")
	if request.method == "POST":
		form = ReplyForm(request.POST)
		if form.is_valid():
			msg = form.save(commit=False)
			msg.author = request.user
			msg.pub_date = timezone.now()
			msg.parent_message = parent_msg
			msg.save()
			return redirect('/messages/'+msg_id+'/')
	raise Http404('invalid use of reply action')

def register(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		def registration_error(error_text, reason):
			return render(request, 'responda_messages/register.html', {
				'registration_error': error_text,
				'error_reason': reason,
				'given_username': username,
				'given_email': email,
				'given_last_name': last_name,
				'given_first_name': first_name})
		if len(first_name) < 1:
			return registration_error('Anna etumimi.', 'first_name')
		if len(password) < 8:
			return registration_error('Salasana on liian lyhyt.', 'password')
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			user = User.objects.create_user(username, email, password)
			user.first_name = first_name
			if len(last_name) > 0: user.last_name = last_name
			user.save()
			auth_login(request, user)
			return redirect('/messages/1/')
		return registration_error('Käyttäjätunnus on varattu.', 'username')
	return render(request, 'responda_messages/register.html', {'registration_error': ''})

def login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return redirect('/messages/1/')
		else:
			return render(request, 'responda_messages/login.html', {'invalidlogin': True, 'given_username': username})
	else:
		return render(request, 'responda_messages/login.html', {'invalidlogin': False})

def logout(request):
	if request.user.is_authenticated:
		auth_logout(request)
	return render(request, 'responda_messages/login.html', {'invalidlogin': False})
